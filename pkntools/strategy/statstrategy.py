__author__ = 'imalkov'
import re
import os

class ThermoProcessor:
    def __init__(self):
        pass

class AgeElvProcessor:
    def __init__(self):
        pass

class PlatoStats:
    def __init__(self, dir_name):
        self.ae_pross = AgeElvProcessor()
        self.t_pross = ThermoProcessor()
        self.dir_name = dir_name

    def make_stats(self, csv_path, context, logger):
        if not os.path.exists(csv_path):
            return False

        plato_path = os.path.join(csv_path, self.dir_name)
        if not os.path.exists(plato_path):
            return False

        
        return True


class CanyonStats:
    def __init__(self):
        self.ae_pross = AgeElvProcessor()
        self.t_pross = ThermoProcessor()

    def make_stats(self, scr_path, context, logger):
        pass