__author__ = 'imalkov'

import os
import sys
sys.path.append(os.getcwd())
from pkntools.mdlutils.mdlcontext import DisplayContext
from .pkngeneric import PknGeneric


class PknDisplay(PknGeneric):
    def __init__(self):
        PknGeneric.__init__(self, DisplayContext(), 'Display')

    def __repr__(self):
        return 'PknDisplay'

    def generate(self, s, logger):
        #plot temperature (x) against depth (y) for all the geotherms
        #plot Age (x) against elevation (y)
        pass

