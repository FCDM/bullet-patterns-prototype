import pygame
import math

from .component import Component

__all__ = ["Circle", "GlowingCircle", "DirectionalLine"]

class Circle(Component):

    def __init__(self, colour, radius):
        self._colour = colour
        self._radius = radius

    def update(self, bullet, time, surface):
        pygame.draw.circle(
            surface, self._colour, tuple(map(int, bullet._origin)), self._radius)


class GlowingCircle(Component):

	def __init__(self, colour, radius):
		self._colour = colour
		self._radius = radius

	def update(self, bullet, time, surface):
		center = tuple(map(int, bullet._origin))
		pygame.draw.circle(
			surface, self._colour, center, self._radius)
		pygame.draw.circle(
			surface, (255, 255, 255), center, self._radius - 2)

class _BaseLine(Component):

	def __init__(self, colour, length, thickness=1):
		self._colour = colour
		self._length = length
		self._thickness = thickness

	def _get_points(self, bullet):
		v = bullet.get_velocity()
		if v is None:
			return v
		m = math.sqrt(v[0]**2 + v[1]**2)/self._length
		x, y = bullet._origin
		x1, y1 = int(x), int(y)
		if m == 0:
			return (x1, y1), (x1, y1)
		x2, y2 = int(x + v[0]/m), int(y + v[1]/m)

		return (x1, y1), (x2, y2)


class DirectionalLine(_BaseLine):

	def __init__(self, colour, length, thickness=1):
		super(DirectionalLine, self).__init__(colour, length, thickness)

	def update(self, bullet, time, surface):
		points = self._get_points(bullet)
		if points is None:
			return
		(x1, y1), (x2, y2) = points

		pygame.draw.line(surface, self._colour, (x1, y1), (x2, y2), self._thickness)
		pygame.draw.circle(surface, self._colour, (x1, y1), int(self._thickness/2) - 1)
		pygame.draw.circle(surface, self._colour, (x2, y2), int(self._thickness/2) - 1)

class GlowingDirectionalLine(_BaseLine):

	def __init__(self, colour, length, thickness=1):
		super(GlowingDirectionalLine, self).__init__(colour, length, thickness)

	def update(self, bullet, time, surface):
		points = self._get_points(bullet)
		if points is None:
			return
		(x1, y1), (x2, y2) = points

		pygame.draw.line(surface, self._colour, (x1, y1), (x2, y2), self._thickness)
		pygame.draw.circle(surface, self._colour, (x1, y1), int(self._thickness/2) - 1)
		pygame.draw.circle(surface, self._colour, (x2, y2), int(self._thickness/2) - 1)

		pygame.draw.line(surface, (255, 255, 255), (x1, y1), (x2, y2), max(self._thickness - 3, 0))
		pygame.draw.circle(surface, (255, 255, 255), (x1, y1), max(int(self._thickness/2) - 3, 0))
		pygame.draw.circle(surface, (255, 255, 255), (x2, y2), max(int(self._thickness/2) - 3, 0))
