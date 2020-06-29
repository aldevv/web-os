import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from scheduler import Scheduler
import unittest

ch = Scheduler()
mem = ch.dispatcher.mem
class MaxTest(unittest.TestCase):

    def testMax(self):
        lines = ["nueva m I 500", "nueva n1 I 100", "nueva ans I 0", "max m n1 ans"]
        ch.compileLines(lines)
        ch.run_all()
        declaration = ch.getDeclaration()
        self.assertEqual(500, declaration.getVariable("ans"))
        ch.resetMaquina()
    
if __name__ == '__main__':
    unittest.main()