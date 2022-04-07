import os
from pathlib import Path

__project__ = 'kMap.py'
__version__ = '2.1.0'
__date__ = '04.04.2022'
__directory__ = Path(os.path.dirname(os.path.realpath(__file__)))

import faulthandler
faulthandler.enable()