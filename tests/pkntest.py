__author__ = 'imalkov'

import unittest
from pekan import PekanSM
from pkntools.mdlutils.mdlcontext import ModelContext

class SMTestCase(unittest.TestCase):
    def test_1_import(self):
        """test PekanSM"""
        machine = PekanSM()
        self.assertEqual(machine.state, None)
        self.assertEqual(isinstance(machine.context, ModelContext), True)




if __name__ == '__main__':
    unittest.main()
