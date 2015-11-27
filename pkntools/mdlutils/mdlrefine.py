__author__ = 'imalkov'

import os, sys

def prepare_to_parse(path):
    res = []
    with open(path) as file:
        lines = file.readlines()
        res = [(line.lstrip()).replace('\n','') for line in lines]
        res = filter(lambda line: False if (len(line) == 0 or line[0] in ['$', '\n']) else True, res)
        res = [line.split('$')[0].strip() for line in res]
    return res

def runcmd(cmd, execdir, short_name = ''):
    pdir = os.getcwd()
    os.chdir(execdir)
    sys.stdout.flush()
    proc = os.popen(cmd)
    s ='---------------------------------- \nhome: {0} --> {1}\ncmd: {2} ' \
       '\n----------------------------------'.format(execdir, short_name, cmd)

    print(s)
    while True:
        line = proc.readline()
        if line != '':
            s += line.strip()
            sys.stdout.flush()
            print('{0} : {1}'.format(short_name,line.strip()))
        else:
            break
    status = proc.close()
    print('ended with status: {0}'.format(status))
    s += 'ended with status: {0}'.format(status)
    os.chdir(pdir)
    return s

def session_naming(path, depth):
    local_path = os.path.abspath(path)
    names_list = str.rsplit(local_path, os.path.sep,depth)[-1 * depth:]
    name = '{0}{1}'.format(names_list[0].replace('NODE','n'), names_list[1].replace('Session', 's'))
    return name

def setvals(src, dst):
    for k, v in src.items():
        setattr(dst, k, v)
    return dst