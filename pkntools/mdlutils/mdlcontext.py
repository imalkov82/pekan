__author__ = 'imalkov'

import os
import ast
import pandas as pnd
from configparser import ConfigParser
import xml.etree.ElementTree as etree

class ModelContext:
    def __init__(self):
        self._context = {}
        self._confobj = None
        self.root = None

    def update(self, context):
        if isinstance(context, dict):
            self._context.update(context)
        elif isinstance(context, ModelContext):
            self._context.update(context._context)
        else:
            raise ValueError('Update Fail: BAD CONTEXT')

    def xml_root(self):
        if self.root != None:
            return self.root
        pekan_xml = self._context['pekan_xml'].replace('~', os.environ['HOME'])
        if not os.path.exists(pekan_xml):
            raise IOError('missing config file')
        root = etree.parse(pekan_xml).getroot()
        self.root = root
        return root

    def col_name(self, name):
        root = self.xml_root()
        states_map = root.find('csv')
        for column in states_map.findall('column'):
            if column.attrib['name'] == name:
                return column.get('value')

    def to_states(self, states_list):
        root = self.xml_root()
        res = []
        states_map = root.find('states_map')
        for state in states_map.findall('state'):
            if state.attrib['name'] not in states_list:
                continue
            res.append((state.find('class').text, int(state.find('rank').text)))
        return [s for s, r in sorted(res, key=lambda s: s[1])]
    #cs file metadata
    @property
    def csv_exec_dir(self):
        return self.col_name('A')
    @property
    def csv_topo_2d_grid_dimentions(self):
        return self.col_name('B')
    @property
    def csv_topo_2d_grid_type(self):
        return self.col_name('C')
    @property
    def csv_create_env(self):
        return self.col_name('D')
    @property
    def csv_topo_2d_max_hights(self):
        return self.col_name('E')
    @property
    def csv_ref_dir(self):
        return self.col_name('F')
    @property
    def csv_test_step(self):
        return self.col_name('G')
    @property
    def csv_pecube_step(self):
        return self.col_name('H')
    @property
    def csv_vtk_step(self):
        return self.col_name('I')
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
                                usecols=[self.csv_exec_dir, self.csv_topo_2d_grid_dimentions,
                                         self.csv_topo_2d_grid_type, self.csv_create_env, self.csv_topo_2d_max_hights,
                                         self.csv_ref_dir])
            tmp_data = data[data[self.csv_create_env] == 1]
            tmp_data[self.csv_exec_dir] = tmp_data[self.csv_exec_dir].apply(lambda x: x.replace('~', os.environ['HOME']))
            tmp_data[self.csv_ref_dir] = tmp_data[self.csv_ref_dir].apply(lambda x: x.replace('~', os.environ['HOME']))
            return tmp_data.drop(self.csv_create_env, axis=1)
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
        data = pnd.read_csv(self._context['peconfig'].replace('~', os.environ['HOME']), header=0, usecols=[self.csv_exec_dir, '{0}'.format(pec_model)])
        work_data = data[data[pec_model] == 1]
        work_data[self.csv_exec_dir] = work_data[self.csv_exec_dir].apply(lambda x: x.replace('~', os.environ['HOME']))
        return [p for i, p in work_data[self.csv_exec_dir].iteritems()]

    @property
    def depth(self):
        return int(self._context['node_depth'])

    @property
    def timeout(self):
        return int(self._context['exec_timeout'])

    @property
    def vtk(self):
        return self._get_wrk_list(self.csv_vtk_step)

    @property
    def pecube(self):
        return self._get_wrk_list(self.csv_pecube_step)

    @property
    def test(self):
        return self._get_wrk_list(self.csv_test_step)

    @property
    def pool_size(self):
        return int(self._context['pool_size'])
