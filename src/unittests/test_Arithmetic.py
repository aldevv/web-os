import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from chmaquina import Chmaquina
import unittest

#test todos los operadores
class ArithmeticTest(unittest.TestCase):
    def clearStaticVariables(self, var):
        var.all_data.clear()
        var.all_data_names.clear()

    def testSume(self):
        ch = Chmaquina()
        mem = ch.mem
        self.clearStaticVariables(ch.variables)
        lines = ["nueva m I 5", "nueva n1 I 10", "cargue m", "sume m"]
        for instruction in lines:
            ch.compileLine(instruction)
        ch.run_all()
        self.assertEqual(10, mem.getAcumulador())
        self.clearStaticVariables(ch.variables)

    def testReste(self):
        instruction_loader = Chmaquina()
        mem = instruction_loader.mem
        self.clearStaticVariables(instruction_loader.variables)
        lines = ["nueva n1 I 25", "nueva m I 40", "cargue m", "reste n1"]
        for instruction in lines:
            instruction_loader.compileLine(instruction)
        instruction_loader.run_all()
        mem.getAcumulador()
        self.assertEqual(15, mem.getAcumulador()) # 40 - 25
        self.clearStaticVariables(instruction_loader.variables)

    def testMult(self):
        instruction_loader = Chmaquina()
        mem = instruction_loader.mem
        self.clearStaticVariables(instruction_loader.variables)
        lines = ["nueva i I 2", "nueva m I 40", "cargue m", "multiplique i"]
        for instruction in lines:
            instruction_loader.compileLine(instruction)
        instruction_loader.run_all()
        self.assertEqual(80, mem.getAcumulador()) # 40 * 2
        self.clearStaticVariables(instruction_loader.variables)

    def testDiv1(self):
        instruction_loader = Chmaquina()
        mem = instruction_loader.mem
        self.clearStaticVariables(instruction_loader.variables)
        lines = ["nueva t I 2", "nueva m I 40", "cargue m", "divida t"]
        for instruction in lines:
            instruction_loader.compileLine(instruction)
        instruction_loader.run_all()
        self.assertEqual(20, mem.getAcumulador()) # 40 / 2
        self.clearStaticVariables(instruction_loader.variables)

    def testDiv2(self):
        instruction_loader = Chmaquina()
        mem = instruction_loader.mem
        self.clearStaticVariables(instruction_loader.variables)
        lines = ["nueva h R 5","nueva t I 2", "cargue h", "divida t"]
        for instruction in lines:
            instruction_loader.compileLine(instruction)
        instruction_loader.run_all()
        self.assertEqual(2.5, mem.getAcumulador()) # 5.0 / 2
        self.clearStaticVariables(instruction_loader.variables)

    def testDiv3(self):
        instruction_loader = Chmaquina()
        mem = instruction_loader.mem
        self.clearStaticVariables(instruction_loader.variables)
        lines = ["nueva h R 27","nueva t I 3", "cargue h", "divida t"]
        for instruction in lines:
            instruction_loader.compileLine(instruction)
        instruction_loader.run_all()
        self.assertEqual(9, mem.getAcumulador()) # 5.0 / 2
        self.clearStaticVariables(instruction_loader.variables)

    def testPow(self):
        instruction_loader = Chmaquina()
        mem = instruction_loader.mem
        self.clearStaticVariables(instruction_loader.variables)
        lines = ["nueva h R -9","nueva t I 2", "cargue h", "potencia t"]
        for instruction in lines:
            instruction_loader.compileLine(instruction)
        instruction_loader.run_all()
        self.assertEqual(81, mem.getAcumulador()) # 5.0 / 2
        self.clearStaticVariables(instruction_loader.variables)

    def testMod(self):
        instruction_loader = Chmaquina()
        mem = instruction_loader.mem
        self.clearStaticVariables(instruction_loader.variables)
        lines = ["nueva h R 0","nueva t I 2", "cargue h", "modulo t"]
        for instruction in lines:
            instruction_loader.compileLine(instruction)
        instruction_loader.run_all()
        self.assertEqual(0, mem.getAcumulador()) # 5.0 / 2
        self.clearStaticVariables(instruction_loader.variables)

if __name__ == '__main__':
    unittest.main()