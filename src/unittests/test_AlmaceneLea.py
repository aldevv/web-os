import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from   chmaquina import Chmaquina
import unittest
import unittest.mock

ch = Chmaquina()
mem = ch.mem
class Almacene_Lea_Test(unittest.TestCase):

    def testAlmacene(self):
        lines = ["nueva m I 5", "nueva n I 20", "cargue m", "almacene n"]
        ch.compileLines(lines)
        ch.run_all()
        declaration = ch.declaration
        self.assertEqual(5, declaration.getVariable('n'))
        ch.resetMaquina()

    # def testLea(self):
    #     ch = Chmaquina()
    #     variables = ch.variables
    #     self.clearStaticVariables(variables)
    #     lines = ["nueva m I 12", "lea m"]
    #     for instruction in lines:
    #         ch.compileLine(instruction)
    #     with unittest.mock.patch('builtins.input', return_value='5'): # just import unittest.mock and use the with
    #         ch.run_all()
    #     self.assertEqual(5, variables.getValue('m'))
    #     self.clearStaticVariables(variables)


if __name__ == '__main__':
    unittest.main()
