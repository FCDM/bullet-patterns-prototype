from .component import CheckAliveComponent

__all__ = ["AliveIfOnScreen"]

class AliveIfOnScreen(CheckAliveComponent):

    def __init__(self, dimensions, offset=100):
        self._dim = [dimensions[0] + offset, dimensions[1] + offset]
        self._offset = offset

    def isAlive(self, bullet, time):
        return (-self._offset <= bullet._origin[0] <= self._dim[0]) and \
            (-self._offset <= bullet._origin[1] <= self._dim[1])