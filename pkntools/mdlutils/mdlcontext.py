__author__ = 'imalkov'

import os
import ast
import pandas as pnd
from configparser import ConfigParser
from .mdlmetainfo import *


class SessionInput:
    def __init__(self, fault_name, topo_name):
        self.topo_name = topo_name
        self.fault_name = fault_name

    @property
    def fault(self):
        return self.fault_name
    @property
    def topo(self):
        return self.topo_name

class Session:
    def __init__(self):
        self.input = SessionInput()

    @property
    def input(self):
        return self.input


class ModelContext:
    def __init__(self):
        self._context = {}
        self._confobj = None
        self.xmlroot = None

    def update(self, context):
        if isinstance(context, dict):
            self._context.update(context)
        elif isinstance(context, ModelContext):
            self._context.update(context._context)
        else:
            raise ValueError('Update Fail: BAD CONTEXT')

    @property
    def csv(self):
        return MetaCsv(self._context['pekan_xml'].replace('~', os.environ['HOME']))

    @property
    def states(self):
        return MetaStateMachine(self._context['pekan_xml'].replace('~', os.environ['HOME']))

    @property
    def pecinput(self):
        return MetaEnvInput(self._context['pekan_xml'].replace('~', os.environ['HOME']))

    @property
    def envinput(self):
        return MetaInputGrid(self._context['pekan_xml'].replace('~', os.environ['HOME']))
    #------------------------------------
    #------------------------------------
    @property
    def class_props(self):
        return

    @property
    def confkls(self):
        return self._confobj

    @property
    def homedir(self):
        return self._context['logging_dir'].replace('~', os.environ['HOME'])

    @confkls.setter
    def confkls(self, val):
        self._confobj = val

class ConvertContext(ModelContext):
    def __init__(self):
        ModelContext.__init__(self)

class DisplayContext(ModelContext):
    def __init__(self):
        ModelContext.__init__(self)

class StatsContext(ModelContext):
    def __init__(self):
        ModelContext.__init__(self)

class HabitatContext(ModelContext):
    def __init__(self):
        ModelContext.__init__(self)

    @property
    def data(self):
        try:
            data = pnd.read_csv(self._context['peconfig'].replace('~', os.environ['HOME']), header=0,
                                usecols=[self.csv.exec_dir, self.csv.topo_2d_grid_dimentions,
                                         self.csv.topo_2d_grid_type, self.csv.create_env, self.csv.topo_2d_max_hights,
                                         self.csv.ref_dir])
            tmp_data = data[data[self.csv.create_env] == 1]
            tmp_data[self.csv.exec_dir] = tmp_data[self.csv.exec_dir].apply(lambda x: x.replace('~', os.environ['HOME']))
            tmp_data[self.csv.ref_dir] = tmp_data[self.csv.ref_dir].apply(lambda x: x.replace('~', os.environ['HOME']))
            return tmp_data.drop(self.csv.create_env, axis=1)
        except Exception as e:
            print(e.args)
            return None

    @property
    def xscale(self):
        return float(self._context['grid_xscale'])

    @property
    def yscale(self):
        return float(self._context['grid_yscale'])

    @property
    def escangle(self):
        return float(self._context['escarpment_angle'])
    @property
    def velangle(self):
        return float(self._context['velo_angle'])

    @property
    def cnynangle(self):
        return float(self._context['canyon_angle'])

    @property
    def bindir(self):
        return self._context['bin_dir'].replace('~', os.environ['HOME'])

    @property
    def topodiff(self):
        try:
            topoconf = ConfigParser()
            topoconf.read(self._context['topo_diff'].replace('~', os.environ['HOME']))
            return dict(topoconf.items('Defaults'))
        except Exception as e:
            print(e.args)
            return None

    @property
    def faultdiff(self):
        try:
            faultconf = ConfigParser()
            faultconf.read(self._context['fault_diff'].replace('~', os.environ['HOME']))
            return dict(faultconf.items('Defaults'))
        except Exception as e:
            print(e.args)
            return None

class NumerExeContext(ModelContext):
    def __init__(self):
        ModelContext.__init__(self)

    def _get_wrk_list(self, pec_model):
        data = pnd.read_csv(self._context['peconfig'].replace('~', os.environ['HOME']), header=0, usecols=[self.csv.exec_dir, '{0}'.format(pec_model)])
        work_data = data[data[pec_model] == 1]
        work_data[self.csv.exec_dir] = work_data[self.csv.exec_dir].apply(lambda x: x.replace('~', os.environ['HOME']))
        return [p for i, p in work_data[self.csv.exec_dir].iteritems()]

    @property
    def depth(self):
        return int(self._context['node_depth'])

    @property
    def timeout(self):
        return int(self._context['exec_timeout'])

    @property
    def vtk(self):
        return self._get_wrk_list(self.csv.vtk_step)

    @property
    def pecube(self):
        return self._get_wrk_list(self.csv.pecube_step)

    @property
    def test(self):
        return self._get_wrk_list(self.csv.test_step)

    @property
    def pool_size(self):
        return int(self._context['pool_size'])
