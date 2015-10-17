__author__ = 'imalkov'

# import pkntools.vtk as vtk
from pkntools.mdlcontext import ConvertContext
from pknstates.pkngeneric import PknGeneric

def convert(s, context, logger):
    pass

class PknConvert(PknGeneric):
    def __init__(self):
        super().__init__(ConvertContext(), 'Convert')

    def generate(self, s, context, logger):
        pass

