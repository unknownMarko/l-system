"""L-systém — deterministický bezkontextový D0L-systém s korytnačou grafikou."""

from .core import rewrite
from .lsystem import Lsystem
from .turtle2d import interpret as interpret_2d, plot as plot_2d
from .turtle3d import interpret as interpret_3d, plot as plot_3d
from .animation import create_gif
from .examples import EXAMPLES
