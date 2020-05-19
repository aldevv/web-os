
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from chmaquina import Chmaquina
import unittest

#test todos los operadores
class MaxTest(unittest.TestCase):
    def clearStaticVariables(self, var):
        var.all_data.clear()
        var.all_data_names.clear()

    def testMax(self):
        ch = Chmaquina()
        variables = ch.variables
        self.clearStaticVariables(ch.variables)
        lines = ["nueva m I 500", "nueva n1 I 100", "nueva ans I 0", "max m n1 ans"]
        for instruction in lines:
            ch.compileLine(instruction)
        ch.run_all()
        self.assertEqual(500, variables.getValue("ans"))
        self.clearStaticVariables(ch.variables)
    
    def testConcatene(self):
        ch = Chmaquina()
        mem = ch.mem
        self.clearStaticVariables(ch.variables)
        lines = ["nueva m C algo",  "concatene esto"]
        for instruction in lines:
            ch.compileLine(instruction)
        ch.run_all()
        self.assertEqual("0esto", mem.getAcumulador())
        self.clearStaticVariables(ch.variables)

    def testElimine1(self):
        ch = Chmaquina()
        variables = ch.variables
        self.clearStaticVariables(ch.variables)
        lines = ["nueva m C algunaClasePizza", "nueva sub C algo", "cargue m", "elimine Clase sub"]
        for instruction in lines:
            ch.compileLine(instruction)
        ch.run_all()
        self.assertEqual("algunaPizza", variables.getValue("sub"))
        self.clearStaticVariables(ch.variables)

    def testElimine2(self):
        ch = Chmaquina()
        variables = ch.variables
        self.clearStaticVariables(ch.variables)
        lines = ["nueva m C algunaClasePizza", "nueva sub C Clase", "cargue m", "elimine sub sub"]
        for instruction in lines:
            ch.compileLine(instruction)
        ch.run_all()
        self.assertEqual("algunaPizza", variables.getValue("sub"))
        self.clearStaticVariables(ch.variables)

    def testExtraiga(self):
        ch = Chmaquina()
        variables = ch.variables
        self.clearStaticVariables(ch.variables)
        lines = ["nueva m C algunaClasePizza", "nueva sub C Clase", "cargue m", "extraiga 5 sub"]
        for instruction in lines:
            ch.compileLine(instruction)
        ch.run_all()
        self.assertEqual("algun", variables.getValue("sub"))
        self.clearStaticVariables(ch.variables)
if __name__ == '__main__':
    unittest.main()