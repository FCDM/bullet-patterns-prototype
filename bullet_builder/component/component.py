import pygame
import math
import abc

__all__ = ["Component", "CheckAliveComponent"]

class Component(object, metaclass=abc.ABCMeta):

	PRECEDENCE = -1

	@abc.abstractmethod
	def update(self, bullet, time, surface):
		pass

class MotionComponent(Component):

	PRECEDENCE = 0

class SpawnComponent(Component):

	PRECEDENCE = 1

class DrawComponent(Component):

	PRECEDENCE = 2


class CheckAliveComponent(object, metaclass=abc.ABCMeta):

	@abc.abstractmethod
	def isAlive(self, bullet):
		pass