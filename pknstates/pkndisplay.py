__author__ = 'imalkov'

import os
import sys
sys.path.append(os.getcwd())
from pkntools.mdlutils.mdlcontext import DispContext
from pknstates.pkngeneric import PknGeneric


class PknDisplay(PknGeneric):
    def __init__(self):
        super().__init__(DispContext(), 'Display')
