__author__ = 'imalkov'

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#      PecUbe Numerous ExecutoR (PUNtER)
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# 2. execution
# 3. logging
# 4. the model will get via cmd the configuration file and logging directory,
# 5. the model will open new file for every step in the execution

import os
import sys
import multiprocessing
sys.path.append(os.getcwd())
from pkntools.mdlutils.mdlcontext import NumerExeContext
from pkntools.mdlutils.mdlrefine import runcmd, session_naming
import pknstates
################################################
class PknExec:
    def __init__(self):
        self.context = NumerExeContext()

    def exec_mdl(self, wrk_list, pool_size, mdl_name, timeout):
        if wrk_list == []:
            return '{0} list is empty'.format(mdl_name)
        cmd = './bin/{0}'.format(mdl_name)
        p = multiprocessing.Pool(min(pool_size, len(wrk_list)))
        results = [p.apply_async(runcmd,args=(cmd,w,session_naming(w, self.context.depth))) for w in wrk_list]
        runcmd_out = [r.get(timeout=timeout) for r in results]
        p.close()
        p.join()
        return runcmd_out

    def __repr__(self):
        return 'PknExec'

    def process(self, remaining_arr, pkn_sm):
        #TODO: pre execution statistics
        pkn_sm.logger.info('process {0}'.format(repr(self)))
        self.context.update(pkn_sm.context)
        self.context.update(dict(pkn_sm.context.confkls['Execution']))
        res_alls = [self.exec_mdl(getattr(self.context, str.lower(exec_name)), self.context.pool_size, exec_name,self.context.timeout)
                    for exec_name in [self.context.csv.test_step, self.context.csv.pecube_step, self.context.csv.vtk_step]]
        try:
            pkn_sm.state = getattr(pknstates, remaining_arr.pop(0))()
        except:
            pkn_sm.state = None