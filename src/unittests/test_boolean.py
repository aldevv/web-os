import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from chmaquina import Chmaquina
import unittest

#test todos los operadores
class BooleanTest(unittest.TestCase):
    def clearStaticVariables(self, var):
        var.all_data.clear()
        var.all_data_names.clear()

    def testAnd(self):
        ch = Chmaquina()
        variables = ch.variables
        self.clearStaticVariables(ch.variables)
        lines = ["nueva m L 5", "nueva n1 L 10", "nueva n2 L 0", "Y m n1 n2"]
        for instruction in lines:
            ch.compileLine(instruction)
        ch.run_all()
        self.assertEqual(True, variables.getValue("n2"))
        self.clearStaticVariables(ch.variables)

    def testOr(self):
        ch = Chmaquina()
        variables = ch.variables
        self.clearStaticVariables(ch.variables)
        lines = ["nueva m L 0", "nueva n1 L 0", "nueva n2 L 0", "O m n1 n2"]
        for instruction in lines:
            ch.compileLine(instruction)
        ch.run_all()
        self.assertEqual(False, variables.getValue("n2"))
        self.clearStaticVariables(ch.variables)

    def testNo(self):
        ch = Chmaquina()
        variables = ch.variables
        self.clearStaticVariables(ch.variables)
        lines = ["nueva m L 0", "nueva n1 L 0", "NO m n1"]
        for instruction in lines:
            ch.compileLine(instruction)
        ch.run_all()
        self.assertEqual(True, variables.getValue("n1"))
        self.clearStaticVariables(ch.variables)

if __name__ == '__main__':
    unittest.main()