# coding=utf8
from __future__ import unicode_literals, absolute_import, division, print_function
"""
These are the core SpiceBot Classes

This module contains references only for other modules to utilize.
"""
# pylama:ignore=W0401,W0611


from .configure import *
from .setup import *
from .shutdown import *

from .Config import *
from .Logs import *
from .Database import *
from .MessageLog import *

from .Update import *
from .osd import *
from .Kick import *

from .Tools import *
from .Prerun import *
from .Commands import *
from .Events import *
from .StartupMonologue import *
from .Server import *
from .Channels import *
from .Users import *
from .AI import *
from .Google import *
from .Gif import *
from .Sherlock import *
from .Reddit import *
from .DictComs import *
from .Read import *
from .Translate import *
from .Version import *
from .RegNicks import *


__author__ = 'Sam Zick'
__email__ = 'sam@deathbybandaid.net'
__version__ = '0.3.0'
