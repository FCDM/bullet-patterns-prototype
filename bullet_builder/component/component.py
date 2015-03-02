import pygame
import math
import abc

__all__ = ["Component", "CheckAliveComponent"]

class Component(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def update(self, bullet, time, surface):
        pass


class CheckAliveComponent(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def isAlive(self, bullet):
        pass