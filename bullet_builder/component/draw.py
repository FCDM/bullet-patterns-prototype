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
		self._prev_point = None

	def _get_points(self, bullet):
		px, py = self._prev_point
		x, y = bullet._origin
		m = math.sqrt((x - px)**2 + (y - py)**2)/self._length
		if m == 0:
			return bullet._origin, bullet._origin
		x1, y1 = int(x), int(y)
		x2, y2 = int(x + (x - px)/m), int(y + (y - py)/m)

		return (x1, y1), (x2, y2)


class DirectionalLine(_BaseLine):

	def __init__(self, colour, length, thickness=1):
		super(DirectionalLine, self).__init__(colour, length, thickness)

	def update(self, bullet, time, surface):
		if self._prev_point is None:
			self._prev_point = bullet._origin[::]
			return

		(x1, y1), (x2, y2) = self._get_points(bullet)

		pygame.draw.line(surface, self._colour, (x1, y1), (x2, y2), self._thickness)
		pygame.draw.circle(surface, self._colour, (x1, y1), int(self._thickness/2) - 1)
		pygame.draw.circle(surface, self._colour, (x2, y2), int(self._thickness/2) - 1)

		self._prev_point = bullet._origin[::]

class GlowingDirectionalLine(_BaseLine):

	def __init__(self, colour, length, thickness=1):
		super(GlowingDirectionalLine, self).__init__(colour, length, thickness)

	def update(self, bullet, time, surface):
		if self._prev_point is None:
			self._prev_point = bullet._origin[::]
			return

		(x1, y1), (x2, y2) = self._get_points(bullet)

		pygame.draw.line(surface, self._colour, (x1, y1), (x2, y2), self._thickness)
		pygame.draw.circle(surface, self._colour, (x1, y1), int(self._thickness/2) - 1)
		pygame.draw.circle(surface, self._colour, (x2, y2), int(self._thickness/2) - 1)

		pygame.draw.line(surface, (255, 255, 255), (x1, y1), (x2, y2), max(self._thickness - 3, 0))
		pygame.draw.circle(surface, (255, 255, 255), (x1, y1), max(int(self._thickness/2) - 3, 0))
		pygame.draw.circle(surface, (255, 255, 255), (x2, y2), max(int(self._thickness/2) - 3, 0))

		self._prev_point = bullet._origin[::]
