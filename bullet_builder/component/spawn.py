import math

from .component import SpawnComponent
from .motion import LinearMotion

import numbers

__all__ = ["LinearShooter", "RotatingShooter", "LinearRadialSpawner", "RotatingRadialSpawner"]

class _BaseSpawner(SpawnComponent):

    def __init__(self, spawn_interval, bullet_speed, bullet_type):
        self._bullet_speed = bullet_speed
        self._bullet_type = bullet_type
        self._spawn_interval = spawn_interval
        self._spawn_interval_is_function = callable(spawn_interval)

    def time_to_generate(self, time):
        if self._spawn_interval_is_function:
            return bool(self._spawn_interval(time))
        return time % self._spawn_interval == 0

class LinearShooter(_BaseSpawner):

    def __init__(self, spawn_interval, direction, bullet_speed, bullet_type):
        super(LinearShooter, self).__init__(spawn_interval, bullet_speed, bullet_type)

        if isinstance(direction, numbers.Real):
            self._dx = math.cos(direction)
            self._dy = math.sin(direction)
        elif isinstance(direction, numbers.Complex):
            self._dx = direction.real
            self._dy = direction.imag
        else:
            self._dx = direction[0]
            self._dy = direction[1]

    def update(self, bullet, time, surface):
        if not self.time_to_generate(bullet._local_time):
            return

        b = self._bullet_type(bullet._origin[0], bullet._origin[1])
        b.add_component(
            LinearMotion(
                (self._dx, self._dy),
                self._bullet_speed))
        bullet.add_child(b)

class RotatingShooter(_BaseSpawner):

    def __init__(self, spawn_interval, initial_direction, bullet_speed, rotation_speed, bullet_type, velocity=True):
        super(RotatingShooter, self).__init__(
            spawn_interval, 
            bullet_speed, 
            bullet_type)
        self._rotation_speed = rotation_speed
        self._current_offset = 0
        self._current_angle = initial_direction
        self._rotation_is_function = callable(rotation_speed)
        self._velocity = velocity

    def update(self, bullet, time, surface):
        if self._rotation_is_function:
            rotation = self._rotation_speed(bullet._local_time)
        else:
            rotation = self._rotation_speed
        if self._velocity:
            self._current_angle += rotation
        else:
            self._current_angle = rotation

        if not self.time_to_generate(bullet._local_time):
            return

        b = self._bullet_type(bullet._origin[0], bullet._origin[1])
        b.add_component(
            LinearMotion(
                (math.cos(self._current_angle),
                 math.sin(self._current_angle)),
                self._bullet_speed))
        bullet.add_child(b)


class _RadialSpawn:

    @staticmethod
    def spawn(bullet, bullet_count, bullet_speed, bullet_type, offset=0):
        angle_increment = 2 * math.pi / bullet_count

        for i in range(bullet_count):
            b = bullet_type(*bullet._origin)
            b.add_component(
                LinearMotion(
                    (math.cos(angle_increment * i + offset),
                     math.sin(angle_increment * i + offset)),
                    bullet_speed))
            bullet.add_child(b)

class LinearRadialSpawner(SpawnComponent):

    def __init__(self, spawn_interval, bullet_count, bullet_speed, bullet_type):
        self._spawn_interval = spawn_interval
        self._bullet_count = bullet_count
        self._bullet_speed = bullet_speed
        self._bullet_type = bullet_type

    def update(self, bullet, time, surface):
        if bullet._local_time % self._spawn_interval != 0:
            return

        _RadialSpawn.spawn(bullet, self._bullet_count, self._bullet_speed, self._bullet_type)


class RotatingRadialSpawner(LinearRadialSpawner):

    def __init__(self, spawn_interval, bullet_count, bullet_speed, rotation_speed, bullet_type):
        super(RotatingRadialSpawner, self).__init__(
            spawn_interval,
            bullet_count,
            bullet_speed,
            bullet_type)
        self._rotation_speed = rotation_speed
        self._current_offset = 0
        self._rotation_is_function = callable(rotation_speed)

    def update(self, bullet, time, surface):
        if self._rotation_is_function:
            rotation = self._rotation_speed(bullet._local_time)
        else:
            rotation = self._rotation_speed
        self._current_offset += rotation
        if bullet._local_time % self._spawn_interval != 0:
            return

        _RadialSpawn.spawn(
            bullet, 
            self._bullet_count, 
            self._bullet_speed, 
            self._bullet_type, 
            self._current_offset)