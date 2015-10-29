__author__ = 'imalkov'

import os
import sys

import numpy as np


def runcmd(cmd, execdir):
    pdir = os.getcwd()
    os.chdir(execdir)
    sys.stdout.flush()
    proc = os.popen(cmd)
    s =''
    while True:
        line = proc.readline()
        if line != '':
            # print(line)
            s += line
            sys.stdout.flush()
        else:
            # print("------------ completed -----------")
            break

    s += 'ended with status: {0}'.format(proc.close())
    os.chdir(pdir)
    return s

def mycallback(cb_res):
    pass
    # print('callback:')
    # print(type(cb_res))
    # if isinstance(cb_res, list):
    #     pass

def f(s, y):
    return s.max()
    # return s.max() - y

from pkntools import vtk
if __name__ == '__main__':
    filename = '/home/imalkov/Dropbox/M.s/Research/DATA/TEST/test01/VTK/Pecube003.vtk'
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(filename)
    print("Reading volume dataset from " + filename + " ...")
    reader.Update()  # executes the reader
    output = reader.GetOutput()
    scalar_range = output.GetScalarRange()
    # ohoh = vtk.PlotOnIntersectionCurves( SliceType="Plane" )
    print(scalar_range)

    # Lx=1345.
    # Ly=1428.
    # x0 = Lx/2.
    # y0 = Ly/2.
    # YA, XA = np.mgrid[0:Ly, 0:Lx]
    # XA = XA - x0
    # YA = YA - y0
    # ang_rot = 23*np.pi/180.
    # XAprim = XA*np.cos(ang_rot) - YA*np.sin(ang_rot)
    # YAprim = XA*np.sin(ang_rot) + YA*np.cos(ang_rot)
    # Theta1 = np.arctan2((YAprim),(XAprim))*-180./np.pi
    #
    # plt.imshow(Theta1,aspect='auto',cmap=plt.cm.hot)
    # plt.colorbar()
    # plt.show()



    # pool = Pool(processes=4)
    # result = pool.apply_async(f, [10])
    # print(result.get(timeout=5))
    # print(pool.map(f, range(10)))
    # df = pandas.read_csv('~/Dropbox/M.s/Research/DOCS/peconfig.csv', header = 0)
    # frame = pandas.DataFrame(numpy.random.randn(4, 3), columns=list('bde'),index=['Utah', 'Ohio', 'Texas', 'Oregon'])
    # print(frame.apply(f, args=(3,), axis=1))

    # wrk_list = ['/home/imalkov/Documents/CODE/PYTHON']
    # cmd = 'python2.7 measure.py'
    # p = multiprocessing.Pool(4)
    #
    # results = [p.apply_async(runcmd,args=(cmd,w), callback=mycallback) for w in wrk_list * 5]
    # try:
    #     res = [r.get(timeout=4) for r in results]
    # except TimeoutError as e:
    #     print(e.args)

    # df = pandas.read_csv('test.csv', header = 0, skipinitialspace = True)
    # print(df['steps'])
    # c = getattr(execrefine, 'AnalysisLogger')()
    # c()


# import multiprocessing
# from os import getpid
#
# def worker(procnum):
#     print('I am number %d in process %d' % (procnum, getpid()))
#     return getpid()
#
# if __name__ == '__main__':
#     pool = multiprocessing.Pool(processes = 3)
#     print(pool.map(worker, range(5)))