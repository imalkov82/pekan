__author__ = 'imalkov'

import os
import sys
sys.path.append(os.getcwd())
from pkntools.mdlcontext import StatsContext
from pkntools.strategy import statstrategy
from pknstates.pkngeneric import PknGeneric



class PknStats(PknGeneric):
    def __init__(self):
        super().__init__(StatsContext(), 'Statistics')
        self.gridtype = {0: 'PlatoStats', 1: 'CanyonStats'}

    def generate(self, s, logger):
        grid = getattr(statstrategy, self.gridtype[int(s['grid_type'])])(self.context, logger)
        grid.make_stats(os.path.join(s['execution_dir'], 'stats'))
