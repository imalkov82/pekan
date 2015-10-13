__author__ = 'imalkov'

import os
import sys
sys.path.append(os.getcwd())
from pkntools.mdlcontext import StatsContext
import pknstates


def genstat(s, context, pknlogger):
    pass

class PknStats:
    def __init__(self):
        self.stats_cnxt = StatsContext()

    def process(self, remaining_arr, pkn_sm):
        self.stats_cnxt.update(pkn_sm.context)
        self.stats_cnxt.update(dict(pkn_sm.context.confkls['Statistics']))
        # self.hbtcnxt.data.apply(genenv, args=(self.hbtcnxt, pkn_sm.logger, ), axis=1)
        self.stats_cnxt.data.apply(genstat, args=(self.stats_cnxt, pkn_sm.logger, ), axis=1)
        # execute code
        try:
            pkn_sm.state = getattr(pknstates, pkn_sm.states_obj[remaining_arr.pop(0)])()
        except:
            pkn_sm.state = None
