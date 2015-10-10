__author__ = 'imalkov'
import os, sys
import ast

class GeneralSM:
    def __init__(self, states_list_str):
        self.state = None
        self.observers = []
        self.states_list_str = states_list_str

    @staticmethod
    def runcmd(cmd):
        sys.stdout.flush()
        print('cmd: {0}'.format(cmd))
        proc = os.popen(cmd)
        while True:
            line = proc.readline()
            if line != '':
                print(line.strip())
                sys.stdout.flush()
            else:
                break
        exec_state = proc.close()
        if exec_state == None:
            print("------------ SUCCESS -----------")
        else:
            raise Exception('fail with {0}'.format(exec_state))

    def update(self):
        for observer in self.observers:
            observer()

    def attach(self, observer):
        self.observers.append(observer)

    def process(self, remaining_list):
        self.update()
        remaining = self.state.process(remaining_list, self)
        if (remaining is not []) and (self.state is not None):
            self.process(remaining)

    def start(self):
        sl = [n.strip() for n in ast.literal_eval(self.states_list_str)]
        self.process(sl)

