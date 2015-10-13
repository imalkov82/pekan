__author__ = 'imalkov'

import os
import sys
sys.path.append(os.getcwd())
from pkntools.mdlcontext import DispContext
import pknstates


class PknDisplay:
    def __init__(self):
        self.disp_cnxt = DispContext()

    def process(self, remaining_arr, pkn_sm):
        self.disp_cnxt.update(pkn_sm.context)
        self.disp_cnxt.update(dict(pkn_sm.context.confkls['Display']))
        # execute code

        try:
            pkn_sm.state = getattr(pknstates, pkn_sm.states_obj[remaining_arr.pop(0)])()
        except:
            pkn_sm.state = None
