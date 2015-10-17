__author__ = 'imalkov'

import os
import sys
sys.path.append(os.getcwd())
from pkntools.mdlcontext import StatsContext
from pkntools.strategy import statstrategy
import pknstates



def genstat(s, context, logger):
    grid = getattr(statstrategy, PknStats.gridtype[int(s['grid_type'])])
    grid.make_stats(s['execution_dir'], context, logger)

class PknStats:
    gridtype = {0: 'PlatoStats',
                1: 'CanyonStats'}
    def __init__(self):
        self.stats_cnxt = StatsContext()

    def process(self, remaining_arr, pkn_sm):
        self.stats_cnxt.update(pkn_sm.context)
        self.stats_cnxt.update(dict(pkn_sm.context.confkls['Statistics']))
        self.stats_cnxt.data.apply(genstat, args=(self.stats_cnxt, pkn_sm.logger, ), axis=1)
        # execute code
        try:
            pkn_sm.state = getattr(pknstates, pkn_sm.states_obj[remaining_arr.pop(0)])()
        except:
            pkn_sm.state = None
