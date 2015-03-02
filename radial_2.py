import bullet_builder as bb
import math

core = bb.BulletCore(400, 100)
game = bb.BulletSimulator((800, 600), core)

class BulletA(bb.Bullet):

	COMPONENTS = [
		bb.component.draw.GlowingCircle((0xFF, 0, 0), 7),
		bb.component.check_alive.AliveIfOnScreen((800, 600))
	]

generator = bb.Bullet(0, 0, parent=core)
generator.add_component(
	bb.component.spawn.RotatingRadialSpawner(5, 30, 4, 1, BulletA)
	)

game.start()