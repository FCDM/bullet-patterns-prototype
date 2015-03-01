import pygame
import math

pygame.init()


class BulletSimulator:

	def __init__(self, dimensions, core, fps=60):
		self._dim = dimensions
		self._running = False
		self._fps = fps
		self.global_time = 0

		self.bullet_core = core

	def start(self):
		SCREEN = pygame.display.set_mode(self._dim)
		CLOCK = pygame.time.Clock()

		self._running = True
		while self._running:

			SCREEN.fill((0, 0, 0))

			for evt in pygame.event.get():
				if evt.type == pygame.QUIT:
					self._running = False

			self.bullet_core.update(self.global_time, SCREEN)

			pygame.display.update()

			CLOCK.tick(self._fps)

			self.global_time += 1
		pygame.quit()

class BulletMeta(type):

	def __new__(metacls, name, bases, kwargs):
		if not kwargs.get("VISIBLE"):
			kwargs["draw"] = lambda self, time, surface: None
		if kwargs.get("STATIC"):
			kwargs["move"] = lambda self, time, surface: None
		if not kwargs.get("GENERATOR"):
			kwargs["spawn"] = lambda self, time, surface: None
		return type.__new__(metacls, name, bases, kwargs)

class Bullet(object, metaclass=BulletMeta):

	def __init__(self, x, y, children=[], parent=None, relative=True):
		self._children = []
		if parent:
			parent.add_child(self)
		if relative and parent:
			self._origin = [x + parent._origin[0], y + parent._origin[1]]
		else:
			self._origin = [x, y]
		for child in children:
			self.add_child(child)
		self._local_time = 0

	def set_parent(self, parent):
		self._parent = parent

	def add_child(self, child):
		self._children.append(child)
		child.set_parent(self)

	def add_children(self, children):
		for child in children:
			self.add_child(child)

	def update(self, time, surface):
		self.draw(time, surface)
		self.move(time, surface)
		self.spawn(time, surface)
		self.extra(time, surface)

		for child in iter(self._children):
			if not child.isAlive():
				self._children.remove(child)
				continue
			child.update(time, surface)

		self._local_time += 1

	def draw(self, time, surface):
		raise NotImplementedError(
			"Method ``draw`` in class ``%s`` is not implemented." % (self.__class__.__name__))

	def move(self, time, surface):
		raise NotImplementedError(
			"Method ``move`` in class ``%s`` is not implemented." % (self.__class__.__name__))

	def spawn(self, time, surface):
		raise NotImplementedError(
			"Method ``spawn`` in class ``%s`` is not implemented." % (self.__class__.__name__))

	def extra(self, time, surface):
		pass

	def isAlive(self):
		return True

class BulletCore(Bullet):
	
	VISIBLE = False
	STATIC = True
	GENERATOR = False

class GeneratorA(Bullet):

	VISIBLE = False
	STATIC = True
	GENERATOR = True

	SPAWN_INTERVAL = 3
	BULLET_COUNT = 40

	def spawn(self, time, surface):
		if time % GeneratorA.SPAWN_INTERVAL != 0:
			return

		angle_increment = 2*math.pi/GeneratorA.BULLET_COUNT

		for i in range(GeneratorA.BULLET_COUNT):
			self.add_child(
				BulletA(
					self._origin[0],
					self._origin[1],
					math.cos(angle_increment*i),
					math.sin(angle_increment*i)
					)
				)

class BulletA(Bullet):

	VISIBLE = True
	STATIC = False
	GENERATOR = False

	SPEED = 8
	RADIUS = 8

	def __init__(self, x, y, vx, vy):
		super(BulletA, self).__init__(x, y)
		self._vx = vx
		self._vy = vy

	def draw(self, time, surface):
		pygame.draw.circle(surface, (0xFF, 0xD9, 0xDA), tuple(map(int, self._origin)), BulletA.RADIUS)

	def move(self, time, surface):
		self._origin[0] += BulletA.SPEED*self._vx
		self._origin[1] += BulletA.SPEED*self._vy

	def isAlive(self):
		return (-100 <= self._origin[0] <= 900) and (-100 <= self._origin[1] <= 700)


core = BulletCore(400, 100)
game = BulletSimulator((800, 600), core)

generator = GeneratorA(0, 0, parent=core)

game.start()

