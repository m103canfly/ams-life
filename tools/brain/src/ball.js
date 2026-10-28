// ams-life (AGPL-3.0); see NOTICE.md.
// The brain map as a ball you can turn and flick, like a globe.
// Pure pieces (no DOM, no three.js), tested from tests/test_brain_page.py:
// - the layout forces that gather the stars into a ball, private ones on one side;
// - the numbers of turning by hand, flicking and spinning by itself.

/** Radius of the ball for n stars: grows with the cube root, so it stays about as dense. */
export function ballRadius(n) {
	return 26 * Math.cbrt(Math.max(n, 50));
}

/**
 * d3-force-3d style force: a star outside the ball is pulled back to it,
 * harder the further out it is. Inside, the stars' own repulsion fills the ball.
 */
export function forceBall(radius, strength) {
	let nodes = [];
	const force = (alpha) => {
		if (!(radius > 0) || !strength) return;
		for (const n of nodes) {
			const x = n.x || 0, y = n.y || 0, z = n.z || 0;
			const r = Math.hypot(x, y, z);
			if (r <= radius || r < 1e-6) continue;
			const k = (strength * alpha * (r - radius)) / r;
			n.vx = (n.vx || 0) - x * k;
			n.vy = (n.vy || 0) - y * k;
			n.vz = (n.vz || 0) - z * k;
		}
	};
	force.initialize = (ns) => { nodes = ns; };
	return force;
}

/** Where along x a star leans: groups (-1) to one side, private chats (+1) to the other, people (0) between. */
export function sideTarget(side, radius) {
	return (side || 0) * radius * 0.42;
}

/** Turning by hand, flicking, spinning by itself. Angles in radians, times in seconds / ms. */
export const SPIN = {
	perScreen: 1.25 * Math.PI,   // dragging across the whole height turns the ball this much
	damping: 1.5,                // a flick slows by e^(-damping * s)
	stopBelow: 0.015,            // rad/s: below this a flick has stopped
	resumeMs: 4000,              // left alone this long, it starts turning by itself again
	rampMs: 2500,                // ... picking up speed over this long
	auto: 0.06,                  // rad/s when turning by itself
};

/** A drag of (dx, dy) px: turn about the screen's up axis (yaw) and right axis (pitch), so the front follows the hand. */
export function dragAngles(dx, dy, height) {
	const k = SPIN.perScreen / Math.max(200, height || 0);
	return { yaw: -dx * k, pitch: -dy * k };
}

/** Speed of a flick after dt seconds more of coasting; 0 once it has nearly stopped. */
export function coast(speed, dt) {
	const s = speed * Math.exp(-SPIN.damping * Math.max(0, dt));
	return Math.abs(s) < SPIN.stopBelow ? 0 : s;
}

/** Speed of turning by itself after idleMs untouched (0 right after a touch). */
export function autoSpeed(idleMs, enabled) {
	if (!enabled || idleMs < SPIN.resumeMs) return 0;
	return SPIN.auto * Math.min(1, (idleMs - SPIN.resumeMs) / SPIN.rampMs);
}
