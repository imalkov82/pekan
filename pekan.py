__author__ = 'imalkov'

# from configparser import ConfigParser
from argparse import ArgumentParser
import ast
import os, sys
import logging


sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from pkntools.mdlutils.mdlcontext import *
import pknstates
# from mdlutils.mdlcontext import *


class PekanSM:
    def __init__(self):
        self.state = None
        self.context = ModelContext()

    def process(self, remaining_list):
        remaining = self.state.process(remaining_list, self)
        if (remaining != []) and (self.state is not None):
            self.process(remaining)

    def _set_configs(self, config_file):
        config = ConfigParser()
        config.read(config_file)
        self.context.confkls = config
        self.context.update(dict(config['Defaults']))

    def _set_logger(self, home_dir):
        if not os.path.exists(home_dir):
            os.mkdir(home_dir)
        logger = logging.getLogger('PEKAN')
        logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        fh = logging.FileHandler(os.path.join(home_dir,'pekan_{0}.log'.format(os.getpid())))
        fh.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(fh)
        logger.addHandler(ch)
        return logger

    def start(self, states_list, config_file):
        self._set_configs(config_file)
        states_obj = self.context.to_states(states_list)
        self.state = getattr(pknstates, states_obj.pop(0))()
        self.logger = self._set_logger(self.context.homedir)
        self.process(states_obj)
        self.logger.info('all states finished')

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-a", dest="config_file", help="configuration file for exucution states")
    parser.add_argument( "-l", dest="states_list", help="list of states to be executed: env, run, display, stat",
                         default='[]')
    kvargs = parser.parse_args()
    pkn = PekanSM()
    pkn.start([n.strip() for n in ast.literal_eval(kvargs.states_list)], kvargs.config_file)