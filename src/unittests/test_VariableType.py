import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from chmaquina import Chmaquina
import unittest

#test nueva y cargue
class VariableTypeTest(unittest.TestCase):
    def clearStaticVariables(self, var):
        var.all_data.clear()
        var.all_data_names.clear()

    def testInt(self):
        ch = Chmaquina()
        variables = ch.variables
        self.clearStaticVariables(ch.variables)
        lines = ["nueva m I 5", "cargue m"]
        for instruction in lines:
            ch.compileLine(instruction)
        self.assertEqual(5, variables.getValue('m'))
        self.assertTrue(type(variables.getValue('m')) is int)
        self.clearStaticVariables(ch.variables)

    def testString(self):
        ch = Chmaquina()
        variables = ch.variables
        self.clearStaticVariables(ch.variables)
        lines = ["nueva n C 5", "cargue n"]
        for instruction in lines:
            ch.compileLine(instruction)
        self.assertEqual("5", variables.getValue('n'))
        self.assertTrue(type(variables.getValue('n')) is str)
        self.clearStaticVariables(ch.variables)


    def testBool(self):
        ch = Chmaquina()
        variables = ch.variables
        self.clearStaticVariables(ch.variables)
        lines = ["nueva o L 0", "cargue o"]
        for instruction in lines:
            ch.compileLine(instruction)
        self.assertEqual(False, variables.getValue('o'))
        self.assertTrue(type(variables.getValue('o')) is bool)
        self.clearStaticVariables(ch.variables)

if __name__ == '__main__':
    unittest.main()
