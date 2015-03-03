import bullet_builder as bb
import math

core = bb.BulletCore(400, 100)
game = bb.BulletSimulator((800, 600), core)

class BulletA(bb.Bullet):

	COMPONENTS = [
		bb.component.draw.GlowingCircle((0x6A, 0x15, 0x86), 7),
		bb.component.check_alive.AliveIfOnScreen((800, 600))
	]

generator = bb.Bullet(0, 0, parent=core)
generator.add_component(
	bb.component.spawn.RotatingRadialSpawner(
		3, 20, 4, 
		bb.functions.SinusoidalWave(20, 2*math.pi/60, 0, -math.pi/60), 
		BulletA))
generator.add_component(
	bb.component.motion.LinearMotion(
		(1, 0), bb.functions.SinusoidalWave(120, 4, 0, -2)))

game.start()