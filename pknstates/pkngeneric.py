__author__ = 'imalkov'

import pknstates

class PknGeneric:
    def __init__(self, context, conftype):
        self.context = context
        self.conftype = conftype

    def generate(self, s, logger):
        pass

    def process(self, remaining_arr, pkn_sm):
        pkn_sm.logger.info('process {0}'.format(repr(self)))
        self.context.update(pkn_sm.context)
        self.context.update(dict(pkn_sm.context.confkls[self.conftype]))
        self.context.data.apply(self.generate, args=(pkn_sm.logger, ), axis=1)
        try:
            pkn_sm.state = getattr(pknstates, pkn_sm.states_obj[remaining_arr.pop(0)])()
        except:
            pkn_sm.state = None