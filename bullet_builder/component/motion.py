import math

from .component import MotionComponent

__all__ = ["LinearMotion", "Orbitter"]

class LinearMotion(MotionComponent):

    def __init__(self, direction, speed):
        self._speed = speed
        self._vx = direction[0]
        self._vy = direction[1]
        if not callable(speed):
            self._vx *= speed
            self._vy *= speed    

    def update(self, bullet, time, surface):
        if callable(self._speed):
            s = self._speed(bullet._local_time)
            bullet._origin[0] += s * self._vx
            bullet._origin[1] += s * self._vy
        else:
            bullet._origin[0] += self._vx
            bullet._origin[1] += self._vy


class Orbitter(MotionComponent):

    def __init__(self, origin, radius, rotation_speed, initial_angle=0, relative_to_parent=True):
        self._origin = origin
        self._radius = radius
        self._rotation_speed = rotation_speed
        self._relative_to_parent = relative_to_parent
        self._current_angle = initial_angle

    def update(self, bullet, time, surface):
        self._current_angle += self._rotation_speed
        if self._relative_to_parent and bullet._parent:
            parent_origin = bullet._parent._origin
        else:
            parent_origin = (0, 0)
        bullet._origin = [
            self._radius *
            math.cos(self._current_angle) + self._origin[0] + parent_origin[0],
            self._radius *
            math.sin(self._current_angle) + self._origin[1] + parent_origin[1]
        ]