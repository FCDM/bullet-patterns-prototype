import pygame
import random
import math

pygame.init()

DIMENSIONS = (800, 600)
SCREEN = pygame.display.set_mode(DIMENSIONS)

CLOCK = pygame.time.Clock()
FPS = 60
GAME_TIME = 0

class Bullet:

	RADIUS = 5

	LIFETIME = 100

	BULLET_SPEED = 1

	def __init__(self, x, y, vx, vy):
		self.x = x
		self.y = y
		self.vx = vx
		self.vy = vy
		self.local_time = 0

	def update(self):
		self.local_time += 1
		self.move()

	def move(self):
		self.x += self.vx
		self.y += self.vy

	def draw(self, surface):
		pygame.draw.circle(surface, Colours.WHITE, (int(self.x), int(self.y)), Bullet.RADIUS)

	def isAlive(self):
		return self.local_time < Bullet.LIFETIME and self.onScreen()

	def onScreen(self):
		return (-100 <= self.x <= DIMENSIONS[0] + 100) and (-100 <= self.y <= DIMENSIONS[1] + 100)

class Comet:

	SPAWN_INTERVAL = 2

	RADIUS = 20

	def __init__(self, x, y, vx, vy):
		self.x = x
		self.y = y
		self.vx = vx
		self.vy = vy
		self.local_time = 0
		self.sparkles = []

	def update(self, time, surface):
		self.local_time += 1
		self.draw(surface)
		for bullet in iter(self.sparkles):
			if not bullet.isAlive():
				self.sparkles.remove(bullet)
				continue
			bullet.draw(surface)
			bullet.update()

		self.spawn(time)
		self.draw(surface)
		self.move()

	def draw(self, surface):
		pygame.draw.circle(surface, Colours.LIGHT_BLUE, (int(self.x), int(self.y)), Comet.RADIUS)

	def spawn(self, time):
		if time % Comet.SPAWN_INTERVAL != 0:
			return
		angle = random.random()*2*math.pi
		self.sparkles.append(
			Bullet(
				self.x, 
				self.y, 
				Bullet.BULLET_SPEED*math.cos(angle) + self.vx, 
				Bullet.BULLET_SPEED*math.sin(angle) + self.vy
				)
			)

	def move(self):
		self.x += self.vx
		self.y += self.vy


class Colours:
	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)
	LIGHT_BLUE = (0xCE, 0xF1, 0xFF)

comet = Comet(400, 100, 0, 1)

RUNNING = True
while RUNNING:
	GAME_TIME += 1
	SCREEN.fill(Colours.BLACK)

	for evt in pygame.event.get():
		if evt.type == pygame.QUIT:
			RUNNING = False

	comet.update(GAME_TIME, SCREEN)

	pygame.display.update()
	CLOCK.tick(FPS)
pygame.quit()