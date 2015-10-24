__author__ = 'imalkov'

from pkntools.mdlutils.mdlcontext import ConvertContext
from pknstates.pkngeneric import PknGeneric


class PknConvert(PknGeneric):
    def __init__(self):
        super().__init__(ConvertContext(), 'Convert')

    def generate(self, s, logger):
        pass



