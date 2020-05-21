import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from chmaquina import Chmaquina
import unittest

ch = Chmaquina()
mem = ch.mem
class MaxTest(unittest.TestCase):

    def clearMemory(self):
        ch.declaration = None
        ch.compiler    = None

    def testMax(self):
        lines = ["nueva m I 500", "nueva n1 I 100", "nueva ans I 0", "max m n1 ans"]
        ch.compileLines(lines)
        ch.run_all()
        declaration = ch.declaration
        self.assertEqual(500, declaration.getVariable("ans"))
        self.clearMemory()
    
if __name__ == '__main__':
    unittest.main()