import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from instruction_loader import Instruction_loader
import unittest

# ingresa 5 para comprobar
class Almacene_Lea_Test(unittest.TestCase):
    def clearStaticVariables(self, var):
        var.all_data.clear()
        var.all_data_names.clear()

    def testAlmacene(self):
        instruction_loader = Instruction_loader()
        variables = instruction_loader.variables
        lines = ["nueva m I 5", "nueva n I 20", "cargue m", "almacene n"]
        for instruction in lines:
            instruction_loader.parse_and_compile(instruction)
        instruction_loader.run_all()
        self.assertEqual(5, variables.getVariable('n'))
        self.clearStaticVariables(variables)

    def testLea(self):
        instruction_loader = Instruction_loader()
        variables = instruction_loader.variables
        lines = ["nueva m I 12", "lea m"]
        for instruction in lines:
            instruction_loader.parse_and_compile(instruction)
        instruction_loader.run_all()
        self.assertEqual(5, variables.getVariable('m'))
        self.clearStaticVariables(variables)


if __name__ == '__main__':
    unittest.main()
