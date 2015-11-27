__author__ = 'imalkov'

import os
import sys
sys.path.append(os.getcwd())
from pkntools.mdlutils.mdlcontext import StatsContext
from pkntools.strategy import statstrategy
from pknstates.pkngeneric import PknGeneric



class PknStats(PknGeneric):
    def __init__(self):
        PknGeneric.__init__(self, StatsContext(), 'Statistics')
        self.grid_type = {0: 'PlatoStats', 1: 'CanyonStats'}

    def __repr__(self):
        return 'PknStats'

    # def generate(self, s, logger):
    #     grid = getattr(statstrategy, self.grid_type[int(
    #         s[self.context.csv_topo_2d_grid_type])])(self.context, logger)
    #     grid.make_stats(os.path.join(s[self.context.csv_exec_dir], 'stats'))
