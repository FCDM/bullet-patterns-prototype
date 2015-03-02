import pygame
import math
import copy
import abc

pygame.init()

from .component import CheckAliveComponent

__all__ = ["BulletSimulator", "Bullet", "BulletCore"]

class BulletSimulator:

    def __init__(self, dimensions, core, fps=60):
        self._dim = dimensions
        self._running = False
        self._fps = fps
        self.global_time = 1

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


class Bullet(object):

    COMPONENTS = []

    def __init__(self, x, y, children=[], parent=None, relative=True):
        self._children = []
        self._parent = parent
        if parent:
            parent.add_child(self)
        if relative and parent:
            self._origin = [x + parent._origin[0], y + parent._origin[1]]
        else:
            self._origin = [x, y]
        for child in children:
            self.add_child(child)
        self._local_time = 1

        self._components = []
        self._check_alive_components = []

        self._extra_init()

    def _extra_init(self):
        for component in self.COMPONENTS:
            if isinstance(component, CheckAliveComponent):
                self.add_check_alive(component)
            else:
                self.add_component(component)

    def set_parent(self, parent):
        self._parent = parent

    def add_child(self, child):
        self._children.append(child)
        child.set_parent(self)

    def add_children(self, children):
        for child in children:
            self.add_child(child)

    def add_component(self, draw_component):
        self._components.append(copy.deepcopy(draw_component))

    def add_check_alive(self, checker):
        self._check_alive_components.append(copy.deepcopy(checker))

    def update(self, time, surface):
        for component in self._components:
            component.update(self, time, surface)

        for child in iter(self._children):
            if not child.isAlive(time):
                self._children.remove(child)
                continue
            child.update(time, surface)

        self._local_time += 1

    def draw(self, time, surface):
        for comp in self._draw_components:
            comp.draw(self, time, surface)

    def move(self, time, surface):
        for comp in self._motion_components:
            comp.move(self, time, surface)

    def spawn(self, time, surface):
        for comp in self._spawn_components:
            comp.spawn(self, time, surface)

    def extra(self, time, surface):
        for comp in self._extra_components:
            comp.extra(self, time, surface)

    def isAlive(self, time):
        return all(comp.isAlive(self, time) for comp in self._check_alive_components)


class BulletCore(Bullet):

    pass

# core = BulletCore(400, 100)
# game = BulletSimulator((800, 600), core)

# generator = Bullet(0, 0, parent=core)
# generator.add_component(LinearMotion((0, 1), 1))
# for i in range(10):
# 	bullet = BulletA(0, 0)
# 	bullet.add_component(
# 		Orbitter([0, 0], 80, 2*math.pi/240, initial_angle=2*math.pi/10 * i))
# 	generator.add_child(bullet)

# game.start()
