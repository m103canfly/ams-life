// ams-life (AGPL-3.0); see NOTICE.md.
// A globe camera for the brain map, in place of Galaxy View's CameraDirector
// (whose OrbitControls stop at the poles and have no flick). Drag to turn the
// ball any way, flick it and it coasts to a stop, wheel or pinch to zoom; left
// alone it turns slowly by itself, and a touch stops it. Turning the ball is
// done by moving the camera round it, so Galaxy View's renderer, picking and
// projection are untouched. The numbers are in ball.js.
import { Quaternion, Vector3 } from 'three';
import { SPIN, autoSpeed, coast, dragAngles } from './ball.js';

const FRAME_MS = 1100;
const ease = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);

export class GlobeCamera {
	constructor(camera, dom) {
		this.camera = camera;
		this.dom = dom;
		this.target = new Vector3();
		this.autoEnabled = true;
		this.spinAxis = new Vector3(0, 1, 0);   // a flick: axis (world) ...
		this.spinSpeed = 0;                      // ... and speed, rad/s
		this.idleMs = SPIN.resumeMs;             // turn by itself from the start
		this.tween = null;
		this.pointers = new Map();
		this.minDist = 5;
		this.maxDist = 50000;
		this.q = new Quaternion();
		this.tmp = new Vector3();
		this.right = new Vector3();
		this.bind();
	}

	// ---- framing
	distanceFor(radius) {
		const vfov = (this.camera.fov * Math.PI) / 180;
		const aspect = Math.max(0.3, Math.min(1, this.camera.aspect || 1));   // narrow screens: fit the width too
		return (Math.max(radius, 1) / Math.sin(vfov / 2)) * 1.25 / aspect;
	}
	setInitial(center, radius) {
		this.target.copy(center);
		const off = this.camera.position.clone().sub(center);
		if (off.lengthSq() < 1e-6) off.set(0.35, 0.45, 1);
		this.camera.position.copy(center).add(off.normalize().multiplyScalar(this.distanceFor(radius)));
		this.camera.lookAt(this.target);
	}
	/**
	 * Fly to look at `center` (radius `radius`). With `towards` (the ball's
	 * centre) the ball turns so that `center` faces the camera.
	 */
	frame(center, radius, towards) {
		const fromOff = this.camera.position.clone().sub(this.target);
		const fromDir = fromOff.clone().normalize();
		let toDir = fromDir.clone();
		if (towards) {
			const out = center.clone().sub(towards);
			if (out.lengthSq() > 1e-6) toDir = out.normalize();
		}
		this.tween = {
			t0: performance.now(), fromTarget: this.target.clone(), toTarget: center.clone(),
			fromDist: fromOff.length(), toDist: this.distanceFor(radius),
			turn: new Quaternion().setFromUnitVectors(fromDir, toDir), fromDir, fromUp: this.camera.up.clone(),
		};
		this.spinSpeed = 0;
		this.idleMs = 0;
	}

	// ---- turning
	/** Turn the camera about a world axis through the target; the ball seems to turn the other way. */
	turn(axis, angle) {
		if (!angle) return;
		this.q.setFromAxisAngle(axis, angle);
		const off = this.camera.position.clone().sub(this.target).applyQuaternion(this.q);
		this.camera.up.applyQuaternion(this.q);
		this.camera.position.copy(this.target).add(off);
		this.camera.lookAt(this.target);
	}
	screenAxes() {
		const fwd = this.tmp.copy(this.target).sub(this.camera.position).normalize();
		this.right.copy(fwd).cross(this.camera.up).normalize();
		const up = this.right.clone().cross(fwd).normalize();
		return { right: this.right.clone(), up };
	}
	dragBy(dx, dy, dtS) {
		const { yaw, pitch } = dragAngles(dx, dy, this.dom.clientHeight);
		const { right, up } = this.screenAxes();
		const rot = up.multiplyScalar(yaw).add(right.multiplyScalar(pitch));   // rotation vector
		const angle = rot.length();
		if (angle < 1e-9) return;
		const axis = rot.normalize();
		this.turn(axis, angle);
		// remember the hand's speed for the flick (smoothed)
		const speed = angle / Math.max(dtS, 1 / 240);
		if (this.spinSpeed > 0 && axis.dot(this.spinAxis) < 0) this.spinSpeed = 0;
		this.spinAxis.lerp(axis, 0.5).normalize();
		this.spinSpeed = this.spinSpeed * 0.4 + speed * 0.6;
	}
	zoomBy(f) {
		const off = this.camera.position.clone().sub(this.target);
		const d = Math.max(this.minDist, Math.min(this.maxDist, off.length() * f));
		this.camera.position.copy(this.target).add(off.setLength(d));
	}

	// ---- input: one pointer turns, two pinch, the wheel zooms
	bind() {
		const dom = this.dom;
		let lastMove = 0, pinch = 0;
		dom.addEventListener('pointerdown', (e) => {
			dom.setPointerCapture?.(e.pointerId);
			this.pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
			this.spinSpeed = 0; this.tween = null; this.idleMs = 0; this.held = true;   // a touch stops it
			lastMove = performance.now();
			if (this.pointers.size === 2) pinch = this.pinchDistance();
		});
		dom.addEventListener('pointermove', (e) => {
			const p = this.pointers.get(e.pointerId);
			if (!p) return;
			const now = performance.now();
			if (this.pointers.size === 1) this.dragBy(e.clientX - p.x, e.clientY - p.y, (now - lastMove) / 1000);
			p.x = e.clientX; p.y = e.clientY;
			if (this.pointers.size === 2) {
				const d = this.pinchDistance();
				if (pinch > 0 && d > 0) this.zoomBy(pinch / d);
				pinch = d;
			}
			lastMove = now;
			this.idleMs = 0;
		});
		const up = (e) => {
			this.pointers.delete(e.pointerId);
			if (this.pointers.size === 0) {
				this.held = false;
				if (performance.now() - lastMove > 90) this.spinSpeed = 0;   // the hand stopped before letting go: no flick
			}
			pinch = 0;
		};
		dom.addEventListener('pointerup', up);
		dom.addEventListener('pointercancel', up);
		dom.addEventListener('wheel', (e) => {
			e.preventDefault();
			this.zoomBy(Math.exp(e.deltaY * 0.0012));
			this.spinSpeed = 0; this.idleMs = 0; this.tween = null;
		}, { passive: false });
	}
	pinchDistance() {
		const [a, b] = [...this.pointers.values()];
		return a && b ? Math.hypot(a.x - b.x, a.y - b.y) : 0;
	}

	// ---- every frame
	update(dtS) {
		const dt = Math.max(0, Math.min(dtS, 0.1));
		if (this.tween) {
			const tw = this.tween;
			const p = Math.min(1, (performance.now() - tw.t0) / FRAME_MS), e = ease(p);
			const q = new Quaternion().slerp(tw.turn, e);   // identity -> turn
			this.target.lerpVectors(tw.fromTarget, tw.toTarget, e);
			const dist = tw.fromDist + (tw.toDist - tw.fromDist) * e;
			this.camera.up.copy(tw.fromUp).applyQuaternion(q);
			this.camera.position.copy(this.target).add(tw.fromDir.clone().applyQuaternion(q).multiplyScalar(dist));
			this.camera.lookAt(this.target);
			if (p >= 1) this.tween = null;
			return;
		}
		if (this.held) return;
		if (this.spinSpeed > 0) {   // coasting after a flick
			this.turn(this.spinAxis, this.spinSpeed * dt);
			this.spinSpeed = coast(this.spinSpeed, dt);
			this.idleMs = 0;
			return;
		}
		this.idleMs += dt * 1000;
		const auto = autoSpeed(this.idleMs, this.autoEnabled);
		if (auto > 0) this.turn(this.camera.up.clone().normalize(), auto * dt);
	}
}
