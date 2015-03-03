import bullet_builder as bb
import math

core = bb.BulletCore(400, 100)
game = bb.BulletSimulator((800, 600), core)

class BulletA(bb.Bullet):

	COMPONENTS = [
		bb.component.draw.GlowingCircle((0, 0x9D, 0xFB), 7),
		bb.component.check_alive.AliveIfOnScreen((800, 600))
	]

generator = bb.Bullet(0, 0, parent=core)
generator.add_component(
	bb.component.spawn.RotatingRadialSpawner(
		3, 20, 6, 
		bb.functions.RectangleWave(20, 2*math.pi/270, 0, -math.pi/270), 
		BulletA))

game.start()