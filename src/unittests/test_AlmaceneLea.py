import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from   chmaquina import Chmaquina
import unittest
import unittest.mock

# ingresa 5 para comprobar
class Almacene_Lea_Test(unittest.TestCase):
    def clearStaticVariables(self, var):
        var.all_data.clear()
        var.all_data_names.clear()

    def testAlmacene(self):
        ch = Chmaquina()
        variables = ch.variables
        self.clearStaticVariables(variables)
        lines = ["nueva m I 5", "nueva n I 20", "cargue m", "almacene n"]
        for instruction in lines:
            ch.compileLine(instruction)
        ch.run_all()
        self.assertEqual(5, variables.getValue('n'))
        self.clearStaticVariables(variables)

    def testLea(self):
        ch = Chmaquina()
        variables = ch.variables
        self.clearStaticVariables(variables)
        lines = ["nueva m I 12", "lea m"]
        for instruction in lines:
            ch.compileLine(instruction)
        with unittest.mock.patch('builtins.input', return_value='5'): # just import unittest.mock and use the with
            ch.run_all()
        self.assertEqual(5, variables.getValue('m'))
        self.clearStaticVariables(variables)


if __name__ == '__main__':
    unittest.main()
