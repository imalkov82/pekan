__author__ = 'imalkov'

import os
import pandas as pnd
from configparser import ConfigParser

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

    @property
    def confkls(self):
        return self._confobj

    @property
    def homedir(self):
        return self._context['logging_dir'].replace('~', os.environ['HOME'])

    @confkls.setter
    def confkls(self, val):
        self._confobj = val

class DispContext(ModelContext):
    def __init__(self):
        super().__init__()

    @property
    def worklist(self):
        work_data = pnd.read_csv(self._context['peconfig'].replace('~', os.environ['HOME']), header=0, usecols=['execution_directory'])
        work_data['execution_directory'] = work_data['execution_directory'].apply(lambda x: x.replace('~', os.environ['HOME']))
        return [p for i, p in work_data['execution_directory'].iteritems()]

class StatsContext(ModelContext):
    def __init__(self):
        super().__init__()

    @property
    def data(self):
        data = pnd.read_csv(self._context['peconfig'].replace('~', os.environ['HOME']), header=0, usecols=['execution_directory', 'grid_type', 'stat'])
        work_data = data[data['stat'] == 1]
        work_data['execution_directory'] = work_data['execution_directory'].apply(lambda x: x.replace('~', os.environ['HOME']))
        return work_data.drop('env', axis=1)
        
class HabitatContext(ModelContext):
    def __init__(self):
        super().__init__()

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
        super().__init__()

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
