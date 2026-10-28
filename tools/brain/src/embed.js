// ams-life (AGPL-3.0); see NOTICE.md.
// The brain map shown inside the panel (pages/dashboard/, "她的脑子").
//
// AstrBot puts each plugin page in an iframe sandboxed without allow-same-origin, so
// the panel's origin is "null", and so is this page's inside it: neither can touch
// the other's objects. The panel builds this page as a srcdoc iframe (a framed page
// of its own would be refused: AstrBot sends X-Frame-Options SAMEORIGIN and
// frame-ancestors 'self', and a "null" parent never matches), so AstrBot's bridge is
// not here at all. Instead the page asks the panel by postMessage, and the panel asks
// AstrBot through its own bridge (pages/dashboard/brain_frame.js): read only, the
// three brain routes, nothing else.
//
// Both origins are "null", so messages are told apart by window, never by origin:
// only what comes from window.parent is read, and messages go only to window.parent,
// with "*" as the target origin because a "null" origin cannot be named.

export const CHANNEL = 'ams-brain';
export const HELLO_MS = 3000;     // no answer from the panel: the sample, saying so
export const ANSWER_MS = 30000;   // a read the panel never answers ends as an error

/** Inside the panel? The panel marks the page it builds (brain_frame.js). */
export function inPanel(doc) {
	return !!(doc && doc.querySelector('meta[name="ams-brain-embed"][content="panel"]'));
}

/** Runs only while every reason to run holds: the panel shows this page ("panel") and
 * the browser tab is visible ("page"). onChange(running) when that flips. */
export function runGate(onChange) {
	const why = { panel: true, page: true };
	let running = true;
	return {
		set(key, on) {
			why[key] = !!on;
			const now = Object.values(why).every(Boolean);
			if (now !== running) { running = now; if (onChange) onChange(now); }
		},
		get running() { return running; },
	};
}

/** A stand-in for AstrBot's bridge that asks the panel: ready() and apiGet() only.
 * on.run(true|false) and on.theme(dark) are what the panel tells the page. */
export function panelBridge(win, on = {}) {
	const parent = win.parent;
	const waiting = new Map();
	let n = 0, hello = null;
	const send = (msg) => parent.postMessage(Object.assign({ channel: CHANNEL }, msg), '*');   // "null": see above
	win.addEventListener('message', (ev) => {
		if (ev.source !== parent) return;
		const m = ev.data;
		if (!m || m.channel !== CHANNEL) return;
		if (m.kind === 'hello' && hello) { const h = hello; hello = null; h({ isDark: !!m.isDark }); }
		else if (m.kind === 'answer' && waiting.has(m.id)) {
			const w = waiting.get(m.id);
			waiting.delete(m.id);
			clearTimeout(w.timer);
			if (m.ok) w.ok(m.data); else w.no(new Error(String(m.error || '面板没取到')));
		} else if (m.kind === 'run' && on.run) on.run(!!m.on);
		else if (m.kind === 'theme' && on.theme) on.theme(!!m.dark);
	});
	return {
		ready() {
			return new Promise((resolve, reject) => {
				hello = resolve;
				send({ kind: 'hello' });
				setTimeout(() => { if (hello) { hello = null; reject(new Error('面板没回音')); } }, HELLO_MS);
			});
		},
		apiGet(route, query) {
			return new Promise((ok, no) => {
				const id = ++n;
				const timer = setTimeout(() => { waiting.delete(id); no(new Error('面板没回音')); }, ANSWER_MS);
				waiting.set(id, { ok, no, timer });
				send({ kind: 'get', id, route: String(route), query: query || {} });
			});
		},
		exitFill() { send({ kind: 'exit-fill' }); },
	};
}
