__author__ = 'imalkov'

import pknstates

class PknGeneric:
    def __init__(self, context, conftype):
        self.context = context
        self.conftype = conftype

    def generate(self, s, logger):
        pass

    def process(self, remaining_arr, pkn_sm):
        self.self.context.update(pkn_sm.context)
        self.self.context.update(dict(pkn_sm.context.confkls[self.conftype]))
        self.self.context.data.apply(self.generate, args=(pkn_sm.logger, ), axis=1)
        try:
            pkn_sm.state = getattr(pknstates, pkn_sm.states_obj[remaining_arr.pop(0)])()
        except:
            pkn_sm.state = None