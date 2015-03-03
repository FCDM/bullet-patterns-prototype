import bullet_builder as bb
import math

core = bb.BulletCore(400, 100)
game = bb.BulletSimulator((800, 600), core)

class BulletA(bb.Bullet):

	COMPONENTS = [
		# bb.component.draw.GlowCircle((0, 0xFB, 0x9D), 7),
		bb.component.draw.GlowingDirectionalLine((0, 0xFB, 0x9D), 20, thickness=10),
		bb.component.check_alive.AliveIfOnScreen((800, 600))
	]

generator = bb.Bullet(0, 0, parent=core)
generator.add_component(
	bb.component.spawn.LinearShooter(4, 3*math.pi/4 - 0.2, 10, BulletA)
	)
generator.add_component(
	bb.component.spawn.RotatingShooter(
		3, math.pi/2, 10, 
		lambda x: 5/8 * math.pi + 1/5*math.sin(x/6) - 0.1, 
		BulletA, velocity=False)
 	)
generator.add_component(
	bb.component.spawn.LinearShooter(4, 5*math.pi/8 - 0.1, 10, BulletA)
	)
generator.add_component(
	bb.component.spawn.LinearShooter(4, math.pi/2, 10, BulletA)
	)
generator.add_component(
	bb.component.spawn.RotatingShooter(
		3, math.pi/2, 10, 
		lambda x: 3/8 * math.pi + 1/5*-math.sin(x/6) + 0.1, 
		BulletA, velocity=False)
 	)
generator.add_component(
	bb.component.spawn.LinearShooter(4, 3*math.pi/8 + 0.1, 10, BulletA)
	)
generator.add_component(
	bb.component.spawn.LinearShooter(4, math.pi/4 + 0.2, 10, BulletA)
	)


game.start()