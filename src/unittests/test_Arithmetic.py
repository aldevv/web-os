import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from chmaquina import Chmaquina
import unittest

ch = Chmaquina()
class ArithmeticTest(unittest.TestCase):

    def testSume(self):
        lines = ["nueva m I 5", "nueva n1 I 10", "cargue m", "sume m"]
        mem = ch.mem
        ch.compileLines(lines)
        ch.run_all()
        self.assertEqual(10, mem.getAcumulador())
        ch.resetMaquina()

    def testReste(self):
        lines = ["nueva n1 I 25", "nueva m I 40", "cargue m", "reste n1"]
        mem = ch.mem
        ch.compileLines(lines)
        ch.run_all()
        self.assertEqual(15, mem.getAcumulador()) # 40 - 25
        ch.resetMaquina()

    def testMult(self):
        lines = ["nueva i I 2", "nueva m I 40", "cargue m", "multiplique i"]
        ch.compileLines(lines)
        ch.run_all()
        mem = ch.mem
        self.assertEqual(80, mem.getAcumulador()) # 40 * 2
        ch.resetMaquina()

    def testDiv1(self):
        lines = ["nueva t I 2", "nueva m I 40", "cargue m", "divida t"]
        ch.compileLines(lines)
        ch.run_all()
        mem = ch.mem
        self.assertEqual(20, mem.getAcumulador()) # 40 / 2
        ch.resetMaquina()

    def testDiv2(self):
        lines = ["nueva h R 5","nueva t I 2", "cargue h", "divida t"]
        ch.compileLines(lines)
        ch.run_all()
        mem = ch.mem
        self.assertEqual(2.5, mem.getAcumulador()) # 5.0 / 2
        ch.resetMaquina()

    def testDiv3(self):
        lines = ["nueva h R 27","nueva t I 3", "cargue h", "divida t"]
        ch.compileLines(lines)
        ch.run_all()
        mem = ch.mem
        self.assertEqual(9, mem.getAcumulador()) # 5.0 / 2
        ch.resetMaquina()

    def testPow(self):
        lines = ["nueva h R -9","nueva t I 2", "cargue h", "potencia t"]
        ch.compileLines(lines)
        ch.run_all()
        mem = ch.mem
        self.assertEqual(81, mem.getAcumulador()) # 5.0 / 2
        ch.resetMaquina()

    def testMod(self):
        lines = ["nueva h R 0","nueva t I 2", "cargue h", "modulo t"]
        ch.compileLines(lines)
        ch.run_all()
        mem = ch.mem
        self.assertEqual(0, mem.getAcumulador()) # 5.0 / 2
        ch.resetMaquina()

if __name__ == '__main__':
    unittest.main()