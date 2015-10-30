# from builtins import float

__author__ = 'imalkov'

import os
import sys
import numpy
sys.path.append(os.getcwd())
from pkntools.mdlutils.mdlcontext import HabitatContext
from pkntools.strategy import gridstrategy
from pkntools.inputrules.faultrule import FaultInput
from pkntools.inputrules.toporule import TopoInput
from pkntools.mdlutils.mdlrefine import runcmd
from pknstates.pkngeneric import PknGeneric

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

class InputNode(EnvNode):
    def __init__(self, path, sample_input, context):
        EnvNode.__init__(self, path)
        self.sample_input = sample_input
        self.context = context

    def __call__(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)
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
        EnvNode.__init__(self, path)
        self.lsteps = lsteps.split('|')
        self.context = context
        self.grid = getattr(gridstrategy, DataNode.gridtype[int(grid)])(dim.split('|')[0], dim.split('|')[1], self.context)

    def __call__(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        try:
            for i, h in enumerate([float(hstr) for hstr in self.lsteps]):
                numpy.savetxt(os.path.join(self.path,'step{0}.txt'.format(i)), self.grid.makegrid(h), fmt='%d')
        except Exception as e:
            print(e.args)

class SrcNode(EnvNode):
    def __init__(self, path, context):
        EnvNode.__init__(self, path)
        self.context = context

    def __call__(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        [runcmd('ln -s {0} {1}'.format(os.path.join(self.context.bindir, cmd), cmd), self.path) for cmd in
               ['Test', 'Pecube', 'Vtk']]


def setvals(src, dst):
    for k, v in src.items():
        setattr(dst, k, v)
    return dst

class PknEnv(PknGeneric):
    def __init__(self):
        PknGeneric.__init__(self, HabitatContext(), 'Environment')

    def __repr__(self):
        return 'PknEnv class'

    def generate(self, s, logger):
        sesion_env = EnvNode(s['execution_directory'])
        sesion_env.attach(InputNode(os.path.join(s['execution_directory'], 'input'),
                           os.path.join(s['sample'], 'input'), self.context))
        sesion_env.attach(SrcNode(os.path.join(s['execution_directory'], 'bin'), self.context))
        sesion_env.attach(DataNode(os.path.join(s['execution_directory'], 'data'), s['dim'], s['steps'],
                             s['grid_type'], self.context))
        sesion_env.attach(EnvNode(os.path.join(s['execution_directory'], 'peout')))
        sesion_env.attach(EnvNode(os.path.join(s['execution_directory'], 'VTK')))
        return sesion_env()