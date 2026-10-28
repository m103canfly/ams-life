// ams-life (AGPL-3.0); see NOTICE.md.
// Fetching her graph from the panel (mixin_brain.py), read only: page/brain in
// parts of one build. Pure (no DOM): `apiGet(route, params)` is the plugin
// page bridge's, or a stand-in in tests/test_brain_page.py.

export const SCHEMA = 'ams-life.brain/1';
export const FETCH = { timeoutMs: 8000, maxParts: 200 };

const unwrap = (r) => (r && r.data !== undefined && r.status !== undefined ? r.data : r);

function withTimeout(p, ms) {
	return Promise.race([p, new Promise((_, rej) => setTimeout(() => rej(new Error('超时')), ms))]);
}

// AstrBot's bridge resolves with the answer's data, and rejects with the message
// when the answer is an error; a stand-in may hand back the whole answer.
async function call(apiGet, params, ms) {
	const r = await withTimeout(apiGet('page/brain', params), ms);
	if (r && r.status === 'error') throw new Error(r.message || '接口出错');
	const d = unwrap(r);
	if (d && d.stale) { const e = new Error('数据更新了'); e.stale = true; throw e; }
	return d;
}

/**
 * The whole graph: part 0, then the other parts of the same build. When the
 * data changed in between (something was deleted), start again once. Throws
 * when the API is not there or says no (the page then shows the sample).
 */
export async function fetchGraph(apiGet, opts) {
	const ms = (opts && opts.timeoutMs) || FETCH.timeoutMs;
	for (let attempt = 0; attempt < 2; attempt++) {
		const first = await call(apiGet, {}, ms);
		if (!first || first.schema !== SCHEMA || !Array.isArray(first.nodes)) throw new Error('不是她的数据');
		const g = Object.assign({}, first, { nodes: first.nodes.slice(), edges: (first.edges || []).slice() });
		const parts = Math.min(FETCH.maxParts, Math.max(1, Number(first.parts) || 1));
		try {
			for (let k = 1; k < parts; k++) {
				const p = await call(apiGet, { part: k, snap: first.snap }, ms);
				g.nodes.push(...(p.nodes || []));
				g.edges.push(...(p.edges || []));
			}
		} catch (e) {
			if (e.stale && attempt === 0) continue;
			throw e;
		}
		delete g.part; delete g.parts; delete g.snap;
		return g;
	}
	throw new Error('数据一直在变');
}

/** The line at the top when the sample is shown instead. */
export function sampleBadge(embedded, why) {
	if (!embedded) return '示例数据（编造）· 不是从 AstrBot 后台打开的';
	return '示例数据（编造）· 接口没连上' + (why ? '：' + why : '');
}
