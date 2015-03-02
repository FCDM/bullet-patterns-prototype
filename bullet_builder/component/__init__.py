__all__ = ["check_alive", "draw", "motion", "spawn"]

from .component import *

from . import check_alive
from . import draw
from . import motion
from . import spawn

__all__.extend(component.__all__)
# __all__.extend(check_alive.__all__)
# __all__.extend(draw.__all__)
# __all__.extend(motion.__all__)
# __all__.extend(spawn.__all__)
