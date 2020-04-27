import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from instruction_loader import Instruction_loader
import unittest

#test todos los operadores
class ArithmeticTest(unittest.TestCase):
    def clearStaticVariables(self, mem):
        mem.variables.all_data.clear()
        mem.variables.all_data_names.clear()

    def testSume(self):
        instruction_loader = Instruction_loader()
        mem = instruction_loader.mem
        lines = ["nueva m I 5", "nueva n1 I 10", "cargue m", "sume m"]
        for instruction in lines:
            instruction_loader.parse_and_compile(instruction)
        instruction_loader.run_all()
        self.assertEqual(10, mem.getAcumulador())
        self.clearStaticVariables(mem)


    def testReste(self):
        instruction_loader = Instruction_loader()
        mem = instruction_loader.mem
        lines = ["nueva n1 I 25", "nueva m I 40", "cargue m", "reste n1"]
        for instruction in lines:
            instruction_loader.parse_and_compile(instruction)
        instruction_loader.run_all()
        mem.getAcumulador()
        self.assertEqual(15, mem.getAcumulador()) # 40 - 25
        self.clearStaticVariables(mem)

    def testMult(self):
        instruction_loader = Instruction_loader()
        mem = instruction_loader.mem
        lines = ["nueva i I 2", "nueva m I 40", "cargue m", "multiplique i"]
        for instruction in lines:
            instruction_loader.parse_and_compile(instruction)
        instruction_loader.run_all()
        self.assertEqual(80, mem.getAcumulador()) # 40 * 2
        self.clearStaticVariables(mem)

    def testDiv1(self):
        instruction_loader = Instruction_loader()
        mem = instruction_loader.mem
        lines = ["nueva t I 2", "nueva m I 40", "cargue m", "divida t"]
        for instruction in lines:
            instruction_loader.parse_and_compile(instruction)
        instruction_loader.run_all()
        self.assertEqual(20, mem.getAcumulador()) # 40 / 2
        self.clearStaticVariables(mem)

    def testDiv2(self):
        instruction_loader = Instruction_loader()
        mem = instruction_loader.mem
        lines = ["nueva h R 5","nueva t I 2", "cargue h", "divida t"]
        for instruction in lines:
            instruction_loader.parse_and_compile(instruction)
        instruction_loader.run_all()
        self.assertEqual(2.5, mem.getAcumulador()) # 5.0 / 2
        self.clearStaticVariables(mem)

    def testDiv3(self):
        instruction_loader = Instruction_loader()
        mem = instruction_loader.mem
        lines = ["nueva h R 27","nueva t I 3", "cargue h", "divida t"]
        for instruction in lines:
            instruction_loader.parse_and_compile(instruction)
        instruction_loader.run_all()
        self.assertEqual(9, mem.getAcumulador()) # 5.0 / 2
        self.clearStaticVariables(mem)

    def testPow(self):
        instruction_loader = Instruction_loader()
        mem = instruction_loader.mem
        lines = ["nueva h R -9","nueva t I 2", "cargue h", "potencia t"]
        for instruction in lines:
            instruction_loader.parse_and_compile(instruction)
        instruction_loader.run_all()
        self.assertEqual(81, mem.getAcumulador()) # 5.0 / 2
        self.clearStaticVariables(mem)

    def testMod(self):
        instruction_loader = Instruction_loader()
        mem = instruction_loader.mem
        lines = ["nueva h R 0","nueva t I 2", "cargue h", "modulo t"]
        for instruction in lines:
            instruction_loader.parse_and_compile(instruction)
        instruction_loader.run_all()
        self.assertEqual(0, mem.getAcumulador()) # 5.0 / 2
        self.clearStaticVariables(mem)

if __name__ == '__main__':
    unittest.main()