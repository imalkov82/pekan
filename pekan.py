__author__ = 'imalkov'

from argparse import ArgumentParser
import ast

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument( "-l", dest="states_list", help="list of states to be executed: run, display, stat",
                         default='[]')
    # parser.add_argument( "-d", action="store_true", dest="debug", help="debug purpose", default= False)

    kvargs = parser.parse_args()
    sl = [n.strip() for n in ast.literal_eval(kvargs.states_list)]

