import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from instruction_loader import Instruction_loader
import unittest

#test nueva y cargue
class VariableTypeTest(unittest.TestCase):
    def testInt(self):
        instruction_loader = Instruction_loader()
        variables = instruction_loader.variables
        lines = ["nueva m I 5", "cargue m"]
        for instruction in lines:
            instruction_loader.parse_and_compile(instruction)
        self.assertEqual(5, variables.all_data['m'])
        self.assertTrue(type(variables.all_data['m']) is int)

    def testString(self):
        instruction_loader = Instruction_loader()
        variables = instruction_loader.variables
        lines = ["nueva n C 5", "cargue n"]
        for instruction in lines:
            instruction_loader.parse_and_compile(instruction)
        self.assertEqual("5", variables.all_data['n'])
        self.assertTrue(type(variables.all_data['n']) is str)


    def testBool(self):
        instruction_loader = Instruction_loader()
        variables = instruction_loader.variables
        lines = ["nueva o L 0", "cargue o"]
        for instruction in lines:
            instruction_loader.parse_and_compile(instruction)
        self.assertEqual(False, variables.all_data['o'])
        self.assertTrue(type(variables.all_data['o']) is bool)

if __name__ == '__main__':
    unittest.main()
