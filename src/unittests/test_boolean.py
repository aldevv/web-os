import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from chmaquina import Chmaquina
import unittest

ch = Chmaquina()
mem = ch.mem
class BooleanTest(unittest.TestCase):

    def testAnd(self):
        lines = ["nueva m L 5", "nueva n1 L 10", "nueva n2 L 0", "Y m n1 n2"]
        ch.compileLines(lines)
        ch.run_all()
        declaration = ch.declaration
        self.assertEqual(True, declaration.getVariable("n2"))
        ch.resetMaquina()

    def testOr(self):
        lines = ["nueva m L 0", "nueva n1 L 0", "nueva n2 L 0", "O m n1 n2"]
        ch.compileLines(lines)
        ch.run_all()
        declaration = ch.declaration
        self.assertEqual(False, declaration.getVariable("n2"))
        ch.resetMaquina()

    def testNo(self):
        lines = ["nueva m L 0", "nueva n1 L 0", "NO m n1"]
        ch.compileLines(lines)
        ch.run_all()
        declaration = ch.declaration
        self.assertEqual(True, declaration.getVariable("n1"))
        ch.resetMaquina()

if __name__ == '__main__':
    unittest.main()