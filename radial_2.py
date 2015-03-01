import pygame
import math

pygame.init()

DIMENSIONS = 800, 600
SCREEN = pygame.display.set_mode(DIMENSIONS)

CLOCK = pygame.time.Clock()
FPS = 60

GAME_TIME = 0


class Colours:
	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)


class Bullet:

	def __init__(self, x, y, vx, vy):
		self.x = x
		self.y = y
		self.vx = vx
		self.vy = vy

	def draw(self, surface):
		pygame.draw.circle(
			surface, Colours.WHITE, (int(self.x), int(self.y)), 8)

	def move(self):
		self.x += self.vx
		self.y += self.vy

	def outsideScreen(self):
		return not ((-100 <= self.x <= DIMENSIONS[0] + 100) and (-100 <= self.y <= DIMENSIONS[1] + 100))


class Spawner:

	BULLET_SPEED = 5
	SPAWN_INTERVAL = 30

	BULLET_COUNT = 30

	ROTATION_SPEED = 1

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.bullets = []

	def spawn(self, time):
		if time % int(Spawner.SPAWN_INTERVAL/Spawner.BULLET_SPEED) != 0:
			return

		angle_increment = 2 * math.pi / Spawner.BULLET_COUNT

		for i in range(Spawner.BULLET_COUNT):
			current_angle = angle_increment * i + time/Spawner.ROTATION_SPEED
			self.bullets.append(Bullet(
				self.x, 
				self.y, 
				Spawner.BULLET_SPEED*math.cos(current_angle), 
				Spawner.BULLET_SPEED*math.sin(current_angle)))

	def update(self, surface):
		for bullet in iter(self.bullets):
			if bullet.outsideScreen():
				self.bullets.remove(bullet)
				continue
			bullet.draw(surface)
			bullet.move()

spawner = Spawner(400, 200)

RUNNING = True

while RUNNING:
	GAME_TIME += 1

	SCREEN.fill(Colours.BLACK)

	for evt in pygame.event.get():
		if evt.type == pygame.QUIT:
			RUNNING = False

	spawner.spawn(GAME_TIME)
	spawner.update(SCREEN)

	pygame.display.update()
	CLOCK.tick(FPS)
pygame.quit()
