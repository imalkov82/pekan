from builtins import float

__author__ = 'imalkov'

import pknstates
import os
import sys
import numpy
sys.path.append(os.getcwd())
from pkntools.mdlcontext import HabitatContext
from pkntools.strategy import gridstrategy
from pkntools.faultrule import FaultInput
from pkntools.toporule import TopoInput
from pkntools.mdlrefine import runcmd


class EnvNode:
    def __init__(self, path):
        self._child_nodes = []
        self.path = path

    def attach(self, env_node):
        self._child_nodes.append(env_node)

    def __call__(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        [node() for node in self._child_nodes]

class SessionEnv(EnvNode):
    def __init__(self, path):
        super().__init__(path)


class InputNode(EnvNode):
    def __init__(self, path, sample_input, context):
        super().__init__(path)
        self.sample_input = sample_input
        self.context = context

    def __call__(self):
        # create fault object
        toposrc = os.path.join(self.sample_input, 'topo_parameters.txt')
        faultsrc = os.path.join(self.sample_input, 'fault_parameters.txt')
        if not all(map(os.path.exists, [toposrc, faultsrc])):
            return
        try:
            setvals(self.context.topodiff, TopoInput(toposrc)).save(os.path.join(self.path,
                                                                                          'topo_parameters.txt'))
            setvals(self.context.faultdiff, FaultInput(faultsrc)).save(os.path.join(self.path,
                                                                                             'fault_parameters.txt'))
        except Exception as e:
            print(e.args)


class DataNode(EnvNode):
    gridtype = {0: 'PlatoGrid',
                1: 'CanyonGrid'}

    def __init__(self, path, dim, lsteps, grid, context):
        super().__init__(path)
        self.lsteps = lsteps.split('|')
        self.context = context
        self.grid = getattr(gridstrategy, DataNode.gridtype[int(grid)])(dim.split('|')[0], dim.split('|')[1], self.context)

    def __call__(self):
        try:
            for i, h in enumerate([float(hstr) for hstr in self.lsteps]):
                numpy.savetxt(os.path.join(self.path,'step{0}.txt'.format(i)), self.grid.makegrid(h), fmt='%d')
        except Exception as e:
            print(e.args)

class SrcNode(EnvNode):
    def __init__(self, path, context):
        super().__init__(path)
        self.context = context

    def __call__(self):
        [runcmd('ln -s {0} {1}'.format(os.path.join(self.context.bindir, cmd), cmd), self.path) for cmd in
               ['Test', 'Pecube', 'Vtk']]


def setvals(src, dst):
    for k, v in src.items():
        setattr(dst, k, v)
    return dst


def genenv(s, context):
    senv = SessionEnv(s['execution_directory'])
    senv.attach(InputNode(os.path.join(s['execution_directory'], 'input'),
                       os.path.join(s['sample'], 'input'), context))
    senv.attach(SrcNode(os.path.join(s['execution_directory'], 'bin'), context))
    senv.attach(DataNode(os.path.join(s['execution_directory'], 'data'), s['dim'], s['steps'],
                         s['grid_type'], context))
    senv.attach(EnvNode(os.path.join(s['execution_directory'], 'peout')))
    senv.attach(EnvNode(os.path.join(s['execution_directory'], 'VTK')))
    return senv()


class PknEnv:
    def __init__(self):
        self.hbtcnxt = HabitatContext()

    def generate(self, s, context, logger):
        print('generate')

    def process(self, remaining_arr, pkn_sm):
        self.hbtcnxt.update(pkn_sm.context)
        self.hbtcnxt.update(dict(pkn_sm.context.confkls['Environment']))
        self.hbtcnxt.data.apply(self.generate, args=(self.hbtcnxt, pkn_sm.logger, ), axis=1)
        try:
            pkn_sm.state = getattr(pknstates, pkn_sm.states_obj[remaining_arr.pop(0)])()
        except:
            pkn_sm.state = None
