__author__ = 'imalkov'

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#      PecUbe Numerous ExecutoR (PUNtER)
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# 1. environment setup
# 2. execution
# 3. logging
# the model will get via cmd the configuration file and logging directory,
# the model will open new file for every step in the execution


import os
import sys
sys.path.append(os.getcwd())
from argparse import ArgumentParser
from configparser import ConfigParser
import pandas as pnd
import multiprocessing

################################################


class Punter:
    def __init__(self, conf_path):
        self._home_dir = os.environ['HOME']
        self._conf = conf_path.replace('~', self._home_dir)

    def process(self):
        # topo_data = pnd.read_csv(self._conf, header=0, usecols=['execution_directory', self._exec_model])
        pass


if __name__ == '__main__':
    parser = ArgumentParser()
    #set cmd rules
    parser.add_argument("-m", dest="pec_model", help="model for execution")
    parser.add_argument("-c", dest="context", help="context pickel file")
    parser.add_argument("-f", dest="log", help="path to log file name")
    kvargs = parser.parse_args()
    #set config rules
    config = ConfigParser()
    config.read('./model.conf')