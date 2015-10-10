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
from mdltools.mdlcontext import NumerExeContext
from mdltools.execrefine import runcmd, session_naming
import pknstates
################################################
class PknExec:
    def __init__(self):
        self.numr_cnxt = NumerExeContext()

    def exec_mdl(self, wrk_list, pool_size, mdl_name, timeout):
        if wrk_list == []:
            return '{0} list is empty'.format(mdl_name)
        cmd = './bin/{0}'.format(mdl_name)
        p = multiprocessing.Pool(min(pool_size, len(wrk_list)))
        results = [p.apply_async(runcmd,args=(cmd,w,session_naming(w, self.numr_cnxt.depth))) for w in wrk_list]
        runcmd_out = [r.get(timeout=timeout) for r in results]
        p.close()
        p.join()
        return runcmd_out

    def process(self, remaining_arr, pkn_sm):
        self.numr_cnxt.update(pkn_sm.context)
        self.numr_cnxt.update(dict(pkn_sm.context.confkls['Execution']))
        for res in [self.exec_mdl(getattr(self.numr_cnxt, str.lower(exec_name)), self.numr_cnxt.pool_size, exec_name,
                                     self.numr_cnxt.timeout) for exec_name in ['Test', 'Pecube', 'Vtk']]:
            pkn_sm.logger.info(res)

        try:
            pkn_sm.state = getattr(pknstates, pkn_sm.states_obj[remaining_arr.pop(0)])()
        except:
            pkn_sm.state = None