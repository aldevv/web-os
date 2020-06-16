
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from chmaquina import Chmaquina
import unittest

ch = Chmaquina()
class StringTest(unittest.TestCase):

    def testConcatene(self):
        lines = ["nueva m C algo",  "concatene esto"]
        ch.compileLines(lines)
        ch.run_all()
        mem = ch.mem
        self.assertEqual("0esto", mem.getAcumulador())
        ch.resetMaquina()

    def testElimine1(self):
        lines = ["nueva m C algunaClasePizza", "nueva sub C algo", "cargue m", "elimine Clase sub"]
        ch.compileLines(lines)
        ch.run_all()
        declaration = ch.declaration
        self.assertEqual("algunaPizza", declaration.getVariable("sub"))
        ch.resetMaquina()

    def testElimine2(self):
        lines = ["nueva m C algunaClasePizza", "nueva sub C Clase", "cargue m", "elimine sub sub"]
        ch.compileLines(lines)
        ch.run_all()
        declaration = ch.declaration
        self.assertEqual("algunaPizza", declaration.getVariable("sub"))
        ch.resetMaquina()

    def testExtraiga(self):
        lines = ["nueva m C algunaClasePizza", "nueva sub C Clase", "cargue m", "extraiga 5 sub"]
        ch.compileLines(lines)
        ch.run_all()
        declaration = ch.declaration
        self.assertEqual("algun", declaration.getVariable("sub"))
        ch.resetMaquina()

if __name__ == '__main__':
    unittest.main()