__author__ = 'imalkov'

from pkntools.mdlutils.mdlcontext import ConvertContext
from pknstates.pkngeneric import PknGeneric


class PknConvert(PknGeneric):
    def __init__(self):
        PknGeneric.__init__(self, ConvertContext(), 'Convert')

    def __repr__(self):
        return 'PknConvert class'

    def generate(self, s, logger):
        pass



