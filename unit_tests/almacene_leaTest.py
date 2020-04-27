import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from instruction_loader import Instruction_loader
import unittest

# ingresa 5 para comprobar
class Almacene_Lea_Test(unittest.TestCase):
    def testAlmacene(self):
        instruction_loader = Instruction_loader()
        variables = instruction_loader.mem.variables
        lines = ["nueva m I 5", "nueva n I 20", "cargue m", "almacene n"]
        for instruction in lines:
            instruction_loader.parse_and_compile(instruction)
        instruction_loader.run_all()
        self.assertEqual(5, variables.all_data['n'])

    def testLea(self):
        instruction_loader = Instruction_loader()
        variables = instruction_loader.mem.variables
        lines = ["lea m"]
        for instruction in lines:
            instruction_loader.parse_and_compile(instruction)
        instruction_loader.run_all()
        self.assertEqual(5, variables.all_data['m'])


if __name__ == '__main__':
    unittest.main()
