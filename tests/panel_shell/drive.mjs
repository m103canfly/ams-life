// Drives the panel shell (serve.py) in a headless Edge / Chrome over its debugging port,
// 127.0.0.1 only, and prints what it saw as one line of JSON. Invented data only.
//
//   node tests/panel_shell/drive.mjs <shell url> <browser exe> <profile dir> [screenshot dir]
//
// Steps: the panel opens (the map not loaded yet) -> "她的脑子" (loaded, live data
// through the panel) -> a person opened, QQ only on the second click -> 铺满, then Esc
// inside the map -> another view (drawing stops) -> back (drawing goes on).
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const [url, exe, profile, shots] = process.argv.slice(2);
const port = 9400 + Math.floor(Math.random() * 400);
const browser = spawn(exe, ['--headless=new', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--no-first-run',
	'--no-default-browser-check', '--remote-debugging-address=127.0.0.1', '--remote-debugging-port=' + port,
	'--user-data-dir=' + profile, '--window-size=1500,950', 'about:blank'], { stdio: 'ignore' });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const out = { steps: {} };
let ws;
try {
	let targets = [];
	for (let i = 0; i < 75 && !targets.length; i++) {
		try { targets = (await (await fetch('http://127.0.0.1:' + port + '/json')).json()).filter((t) => t.type === 'page'); } catch { /* starting */ }
		if (!targets.length) await sleep(200);
	}
	ws = new WebSocket(targets[0].webSocketDebuggerUrl);
	await new Promise((r) => ws.addEventListener('open', r));
	let id = 0;
	const pending = new Map();
	const contexts = [];   // {session, id} of every frame's main world
	const errors = [];
	const send = (method, params = {}, sessionId) => new Promise((r) => {
		const i = ++id;
		pending.set(i, r);
		ws.send(JSON.stringify(Object.assign({ id: i, method, params }, sessionId ? { sessionId } : {})));
	});
	ws.addEventListener('message', async (e) => {
		const m = JSON.parse(e.data);
		if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); return; }
		if (m.method === 'Runtime.executionContextCreated' && m.params.context.auxData && m.params.context.auxData.isDefault) {
			contexts.push({ session: m.sessionId, id: m.params.context.id });
		}
		if (m.method === 'Runtime.executionContextDestroyed') {
			const k = contexts.findIndex((c) => c.session === m.sessionId && c.id === m.params.executionContextId);
			if (k >= 0) contexts.splice(k, 1);
		}
		if (m.method === 'Runtime.exceptionThrown') errors.push(String(m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text).slice(0, 200));
		if (m.method === 'Target.attachedToTarget') {   // a frame in a process of its own
			const s = m.params.sessionId;
			await send('Runtime.enable', {}, s);
			await send('Target.setAutoAttach', { autoAttach: true, waitForDebuggerOnStart: false, flatten: true }, s);
		}
	});
	await send('Runtime.enable');
	await send('Page.enable');
	await send('Target.setAutoAttach', { autoAttach: true, waitForDebuggerOnStart: false, flatten: true });
	await send('Emulation.setDeviceMetricsOverride', { width: 1500, height: 950, deviceScaleFactor: 1, mobile: false });
	await send('Page.navigate', { url });
	await sleep(3000);

	const evalIn = async (c, expr) => {
		const r = await send('Runtime.evaluate', { expression: expr, contextId: c.id, returnByValue: true, awaitPromise: true }, c.session);
		return r.result && !r.result.exceptionDetails ? r.result.result.value : undefined;
	};
	const find = async (test) => {   // the frame where `test` is true
		for (let k = 0; k < 40; k++) {
			for (const c of [...contexts]) if (await evalIn(c, test) === true) return c;
			await sleep(250);
		}
		throw new Error('no frame for ' + test);
	};
	const shot = async (name) => {
		if (!shots) return;
		const r = await send('Page.captureScreenshot', { format: 'png' });
		fs.writeFileSync(path.join(shots, name), Buffer.from(r.result.data, 'base64'));
	};
	const host = await find('!!window.__hostLog');
	const panel = await find("!!document.getElementById('brainBox')");
	out.steps.before = await evalIn(panel, `({ frames: document.querySelectorAll('#brainBox iframe').length,
		nav: [...document.querySelectorAll('.nav-item')].map((b) => b.dataset.view),
		fillLabel: document.getElementById('brainFill').textContent })`);

	await evalIn(panel, "document.querySelector('.nav-item[data-view=brain]').click()");
	const brain = await find("!!(window.__brain && document.getElementById('statLine'))");
	await sleep(4000);
	out.steps.opened = await evalIn(brain, `({ running: window.__brain.running, frames: window.__brain.frames,
		badge: document.getElementById('sourceBadge').hidden ? '' : document.getElementById('sourceBadge').textContent,
		stat: document.getElementById('statLine').textContent, size: [innerWidth, innerHeight],
		agentBridge: !!window.AstrBotPluginView })`);
	out.steps.panelScroll = await evalIn(panel, '[document.scrollingElement.scrollHeight, innerHeight, getComputedStyle(document.body).overflow]');
	await shot('1-面板里点开她的脑子.png');

	// a person: opened, then the QQ number on its own click
	await evalIn(brain, "document.getElementById('q').value = '人'; document.getElementById('q').dispatchEvent(new Event('input'))");
	await sleep(1200);
	await evalIn(brain, "(document.querySelector('#hits li[data-id^=\"p:\"]') || document.querySelector('#hits li[data-id]')).click()");
	await sleep(1500);
	out.steps.person = await evalIn(brain, `({ title: document.getElementById('dTitle').textContent,
		qqShownBefore: /示例-\\d+/.test(document.getElementById('drawer').textContent), button: !!document.getElementById('qqBtn') })`);
	await evalIn(brain, "document.getElementById('qqBtn') && document.getElementById('qqBtn').click()");
	await sleep(1200);
	out.steps.person.qqAfter = await evalIn(brain, "document.getElementById('qqVal') ? document.getElementById('qqVal').textContent : ''");

	// 铺满, then Esc pressed inside the map
	const w0 = await evalIn(brain, 'innerWidth');
	await evalIn(panel, "document.getElementById('brainFill').click()");
	await sleep(1500);
	out.steps.filled = await evalIn(panel, "({ filled: document.body.classList.contains('brain-filled'), label: document.getElementById('brainFill').textContent })");
	out.steps.filled.widthBefore = w0;
	out.steps.filled.widthAfter = await evalIn(brain, 'innerWidth');
	await shot('2-铺满.png');
	await evalIn(brain, "window.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }))");
	await sleep(800);
	out.steps.escaped = await evalIn(panel, "({ filled: document.body.classList.contains('brain-filled'), label: document.getElementById('brainFill').textContent })");
	out.steps.escaped.width = await evalIn(brain, 'innerWidth');

	// another view: drawing stops; back: it goes on
	await evalIn(panel, "document.querySelector('.nav-item[data-view=overview]').click()");
	await sleep(600);
	const f1 = await evalIn(brain, 'window.__brain.frames');
	await sleep(1500);
	const f2 = await evalIn(brain, 'window.__brain.frames');
	out.steps.away = { running: await evalIn(brain, 'window.__brain.running'), framesWhileAway: f2 - f1 };
	await evalIn(panel, "document.querySelector('.nav-item[data-view=brain]').click()");
	await sleep(1500);
	out.steps.back = { running: await evalIn(brain, 'window.__brain.running'), framesAfter: (await evalIn(brain, 'window.__brain.frames')) - f2,
		framesInPanel: await evalIn(panel, "document.querySelectorAll('#brainBox iframe').length") };
	await shot('3-切走再切回来.png');

	out.host = await evalIn(host, 'window.__hostLog');
	out.errors = errors;
} catch (e) {
	out.failed = String(e && e.message || e);
} finally {
	try { ws && ws.close(); } catch { /* closed */ }
	browser.kill();
}
process.stdout.write(JSON.stringify(out) + '\n');
