__author__ = 'imalkov'
import os
import sys
import numpy

sys.path.append(os.getcwd())
from pkntools.mdlutils.mdlcontext import HabitatContext
from pkntools.mdlutils.mdlrefine import setvals
from pkntools.strategy import gridstrategy
from pkntools.inputrules.faultrule import FaultInput
from pkntools.inputrules.toporule import TopoInput
from pkntools.mdlutils.mdlrefine import runcmd
from .pkngeneric import PknGeneric


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
        toposrc = os.path.join(self.sample_input, self.context.pecinput.topofile)
        faultsrc = os.path.join(self.sample_input, self.context.pecinput.faultfile)
        if not all(map(os.path.exists, [toposrc, faultsrc])):
            return
        try:
            setvals(self.context.topodiff, TopoInput(toposrc)).save(
                os.path.join(self.path,self.context.pecinput.topofile))
            setvals(self.context.faultdiff, FaultInput(faultsrc)).save(
                os.path.join(self.path,self.context.pecinput.faultfile))

        except Exception as e:
            print(e.args)


class DataNode(EnvNode):
    def __init__(self, path, dim, lsteps, grid, context):
        EnvNode.__init__(self, path)
        self.lsteps = lsteps.split('|')
        self.context = context
        self.grid = getattr(gridstrategy, self.context.envinput.gridtype(grid))(dim.split('|')[0], dim.split('|')[1],self.context)

    def __call__(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        try:
            for i, h in enumerate([float(hstr) for hstr in self.lsteps]):
                numpy.savetxt(os.path.join(self.path, 'step{0}.txt'.format(i)), self.grid.makegrid(h), fmt='%d')
        except Exception as e:
            print(e.args)


class SrcNode(EnvNode):
    def __init__(self, path, context):
        EnvNode.__init__(self, path)
        self.context = context

    def __call__(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        else:
            runcmd('rm {0}/*'.format(self.path), self.path)
        # execute
        [runcmd('ln -s {0} {1}'.format(os.path.join(self.context.bindir, cmd), cmd), self.path) for cmd in
         [self.context.csv.test_step, self.context.csv.pecube_step, self.context.csv.vtk_step]]


class PknEnv(PknGeneric):
    def __init__(self):
        PknGeneric.__init__(self, HabitatContext(), 'Environment')

    def __repr__(self):
        return 'PknEnv'

    def generate(self, s, logger):
        sesion_env = EnvNode(s[self.context.csv.exec_dir])
        sesion_env.attach(InputNode(os.path.join(s[self.context.csv.exec_dir], 'input'),
                                    os.path.join(s[self.context.csv.ref_dir], 'input'), self.context))
        sesion_env.attach(SrcNode(os.path.join(s[self.context.csv.exec_dir], 'bin'), self.context))
        sesion_env.attach(DataNode(os.path.join(s[self.context.csv.exec_dir], 'data'),
                                   s[self.context.csv.topo_2d_grid_dimentions],
                                   s[self.context.csv.topo_2d_max_hights],
                                   s[self.context.csv.topo_2d_grid_type], self.context))
        sesion_env.attach(EnvNode(os.path.join(s[self.context.csv.exec_dir], 'peout')))
        sesion_env.attach(EnvNode(os.path.join(s[self.context.csv.exec_dir], 'VTK')))
        return sesion_env()
