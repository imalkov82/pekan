__author__ = 'imalkov'
import re
import os
import pandas as pnd

class PropsProcessor:
    def __init__(self, metrica):
        self.metrica = metrica
        self.extension = 'csv'

    def collect(self, path):
        self.mtrx_dict = {}
        r = re.compile('{0}\d.{1}'.format(self.metrica, self.extension))
        for root, dirs, files in os.listdir(path):
            return sorted([os.path.join(root,x) for x in files if r.match(x)])

class AgeElevationProcessor(PropsProcessor):
    def __init__(self, metrica):
        super().__init__(metrica)
        self.columns = ['ExhumationRate', 'ApatiteHeAge', 'Points:2', 'arc_length']

    def __call__(self, path):
        self.collect(path)
        for k, v in self.mtrx_dict.items():
            for f in v:
                df = pnd.read_csv(f, header = 0, usecols= self.columns)

class TemperatureProcessor(PropsProcessor):
    def __init__(self, metrica):
        super().__init__(metrica)
        self.columns = ['velo:0', 'velo:1', 'velo:2', 'arc_length', 'Points:2']

    def __call__(self, path):
        self.collect(path)
        for k, v in self.mtrx_dict.items():
            for f in v:
                df = pnd.read_csv(f, header = 0, usecols= self.columns)

class EscarpmentStats:
    '''
    metrics to be extracted:
        1. denudation rate
            a. expected (from fault_input.txt, topo_input.txt)
            b. model (Age-Elevation.csv)
            c. diff in %
        2. exhumation rate (escarpment)
            a. expected (from fault_input.txt, topo_input.txt)
            b. model (Age-Elevation.csv)
            c. diff in %
        3. isotherma depth (footwall)
            a.
            '''
    def __init__(self, context, logger):
        self.context = context
        self.logger = logger
        self.types = {'Age-Elevation': 'AgeElevationProcessor', 'Temperature': 'TemperatureProcessor'}

    def make_stats(self, path):
        if not os.path.exists(path):
            return False
        #stats on Age-Elevation,
        #stats on Temperature depth
        #stats on corelative data
        return True


class CanyonStats:
    def __init__(self):
        pass

    def make_stats(self, scr_path, context, logger):
        pass