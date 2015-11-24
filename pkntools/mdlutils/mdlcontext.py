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

    def update(self, context):
        if isinstance(context, dict):
            self._context.update(context)
        elif isinstance(context, ModelContext):
            self._context.update(context._context)
        else:
            raise ValueError('Update Fail: BAD CONTEXT')

    def to_states(self, states_list):
        pekan_xml = self._context['pekan_xml'].replace('~', os.environ['HOME'])
        if not os.path.exists(pekan_xml):
            raise IOError('missing config file')

        res = []
        root = etree.parse(pekan_xml).getroot()
        for state in root.findall('state'):
            if state.attrib['name'] not in states_list:
                continue
            res.append((state.find('class').text, int(state.find('rank').text)))
        return [s for s, r in sorted(res, key=lambda s: s[1])]


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

class DispContext(ModelContext):
    def __init__(self):
        ModelContext.__init__(self)

    @property
    def worklist(self):
        work_data = pnd.read_csv(self._context['peconfig'].replace('~', os.environ['HOME']), header=0, usecols=['execution_directory'])
        work_data['execution_directory'] = work_data['execution_directory'].apply(lambda x: x.replace('~', os.environ['HOME']))
        return [p for i, p in work_data['execution_directory'].iteritems()]

class StatsContext(ModelContext):
    def __init__(self):
        ModelContext.__init__(self)

    def metrics(self):
        if 'metrics' not in self._context:
            raise ValueError('metrics not in configuration')
        res = {}
        for k,v in ast.literal_eval(self._context['metrics']).items():
            res[k] = ast.literal_eval(v)
        return res

    @property
    def data(self):
        data = pnd.read_csv(self._context['peconfig'].replace('~', os.environ['HOME']), header=0, usecols=['execution_directory', 'grid_type', 'stat'])
        work_data = data[data['stat'] == 1]
        work_data['execution_directory'] = work_data['execution_directory'].apply(lambda x: x.replace('~', os.environ['HOME']))
        return work_data.drop('env', axis=1)
        
class HabitatContext(ModelContext):
    def __init__(self):
        ModelContext.__init__(self)

    @property
    def data(self):
        try:
            data = pnd.read_csv(self._context['peconfig'].replace('~', os.environ['HOME']), header=0,
                                usecols=['execution_directory', 'dim', 'grid_type', 'env', 'steps', 'sample'])
            tmp_data = data[data['env'] == 1]
            tmp_data['execution_directory'] = tmp_data['execution_directory'].apply(lambda x: x.replace('~', os.environ['HOME']))
            tmp_data['sample'] = tmp_data['sample'].apply(lambda x: x.replace('~', os.environ['HOME']))
            return tmp_data.drop('env', axis=1)
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
        data = pnd.read_csv(self._context['peconfig'].replace('~', os.environ['HOME']), header=0, usecols=['execution_directory', '{0}'.format(pec_model)])
        work_data = data[data[pec_model] == 1]
        work_data['execution_directory'] = work_data['execution_directory'].apply(lambda x: x.replace('~', os.environ['HOME']))
        return [p for i, p in work_data['execution_directory'].iteritems()]

    @property
    def depth(self):
        return int(self._context['node_depth'])

    @property
    def timeout(self):
        return int(self._context['exec_timeout'])

    @property
    def vtk(self):
        return self._get_wrk_list('Vtk')

    @property
    def pecube(self):
        return self._get_wrk_list('Pecube')

    @property
    def test(self):
        return self._get_wrk_list('Test')

    @property
    def pool_size(self):
        return int(self._context['pool_size'])
