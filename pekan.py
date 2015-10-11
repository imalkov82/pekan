__author__ = 'imalkov'

from pkntools.mdlcontext import *
import pknstates
from configparser import ConfigParser
from argparse import ArgumentParser
import ast
import os, sys
import logging

class PekanSM:
    def __init__(self):
        self.state = None
        self.context = ModelContext()
        self.states_rank = {'env': 0, 'run': 1, 'stat': 2, 'display': 3}
        self.states_obj = {'env': 'PknEnv', 'run': 'PknExec', 'stat': 'PknStats', 'display': 'PknDisplay'}

    def process(self, remaining_list):
        remaining = self.state.process(remaining_list, self)
        if (remaining != []) and (self.state is not None):
            self.logger.info('pekan_sm process')
            self.process(remaining)
        self.logger.info('pekan_sm finished')

    def _set_state(self, states_list):
        sl_kv = [(s, self.states_rank[s]) for s in set(states_list)]
        sl = [s for s,r in sorted(sl_kv, key=lambda s: s[1])]
        return getattr(pknstates, self.states_obj[sl.pop(0)])(), sl

    def _set_configs(self, config_file):
        config = ConfigParser()
        config.read(config_file)
        self.context.confkls = config
        self.context.update(dict(config['Defaults']))

    def _set_logger(self, home_dir):
        if not os.path.exists(home_dir):
            os.mkdir(home_dir)
        log_name = os.path.join(home_dir,'pekan_{0}.log'.format(os.getpid()))
        logging.basicConfig(filename=log_name,level=logging.DEBUG)
        # logging.basicConfig(filename=sys.stdout, level=logging.DEBUG)
        return logging.getLogger('PEKAN')

    def start(self, states_list, config_file):
        self.state, sl = self._set_state(states_list)
        self._set_configs(config_file)
        self.logger = self._set_logger(self.context.homedir)
        self.process(sl)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-a", dest="config_file", help="configuration file for exucution states")
    parser.add_argument( "-l", dest="states_list", help="list of states to be executed: env, run, display, stat",
                         default='[]')
    # parser.add_argument( "-d", action="store_true", dest="debug", help="debug purpose", default= False)
    kvargs = parser.parse_args()
    pkn = PekanSM()
    pkn.start([n.strip() for n in ast.literal_eval(kvargs.states_list)], kvargs.config_file)