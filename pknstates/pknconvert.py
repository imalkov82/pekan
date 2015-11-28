__author__ = 'imalkov'

from pkntools.mdlutils.mdlcontext import ConvertContext
from .pkngeneric import PknGeneric


class PknConvert(PknGeneric):
    def __init__(self):
        PknGeneric.__init__(self, ConvertContext(), 'Convert')

    def __repr__(self):
        return 'PknConvert'

    def generate(self, s, logger):
        pass



