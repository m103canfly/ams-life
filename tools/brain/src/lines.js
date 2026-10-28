// ams-life (AGPL-3.0); see NOTICE.md.
// Which lines the brain map draws, and how strongly. Usually none: the stars
// stand alone and she only "connects" when something is called up -- a turn she
// recalled, or a star the owner opened. The layout still uses every relation to
// place related stars together; only the drawing is decided here.
// Pure functions (no DOM, no three.js), tested from tests/test_brain_page.py.

/** "Show all lines" is only for the owner to check things; off unless switched on. */
export const SHOW_ALL_DEFAULT = false;

/** One turn, in ms: a recalled star every `step`, then `hold`, then the lines fade over `fade`. */
export const TURN = { step: 600, hold: 1800, fade: 1600, rest: 900 };

/** The base layer of every line is drawn only when the owner switched it on. */
export function baseLinesVisible(showAll) {
	return showAll === true;
}

/** "a:b" and "b:a" -> index of the line between a and b. */
export function lineMap(links) {
	const m = new Map();
	links.forEach((l, i) => {
		m.set(l.source + ':' + l.target, i);
		m.set(l.target + ':' + l.source, i);
	});
	return m;
}

/** The lines she went along in one turn, in order. Never one to or from a held-back star. */
export function turnSteps(map, path, held) {
	const h = new Set(held);
	const out = [];
	for (const [a, b] of path) {
		if (h.has(a) || h.has(b)) continue;
		const line = map.get(a + ':' + b);
		if (line !== undefined && !out.some((s) => s.line === line)) out.push({ a, b, line });
	}
	return out;
}

/** How long one turn plays before the next one starts. */
export function turnLength(recalled) {
	return Math.max(1, recalled) * TURN.step + TURN.hold + TURN.fade + TURN.rest;
}

/**
 * One moment of a turn: how many recalled stars are lit, which lines are drawn
 * and how strongly (alpha), and whether it is over. Without motion everything
 * is shown at once and stays.
 */
export function turnFrame(steps, recalled, local, motion) {
	if (!motion) return { lit: recalled, lines: steps.map((s) => s.line), alpha: 1, done: false };
	const lit = Math.min(recalled, Math.floor(local / TURN.step) + 1);
	const end = Math.max(1, recalled) * TURN.step + TURN.hold;
	const alpha = local <= end ? 1 : Math.max(0, 1 - (local - end) / TURN.fade);
	const lines = alpha > 0 ? steps.filter((s, k) => local >= (k + 0.5) * TURN.step).map((s) => s.line) : [];
	return { lit, lines, alpha, done: local >= turnLength(recalled) };
}

/**
 * A star the owner opened: the lines it can call up -- its associations, or,
 * when it has none (a person, a window, an event), its own lines.
 */
export function openedLines(links, i) {
	const assoc = [];
	const own = [];
	links.forEach((l, li) => {
		if (l.source !== i && l.target !== i) return;
		own.push(li);
		if (l.kind === 'link') assoc.push(li);
	});
	return assoc.length ? assoc : own;
}
