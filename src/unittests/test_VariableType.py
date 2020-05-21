import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from chmaquina import Chmaquina
import unittest

ch = Chmaquina()
mem = ch.mem
class VariableTypeTest(unittest.TestCase):
    def clearMemory(self):
        ch.declaration = None
        ch.compiler    = None

    def testInt(self):
        lines = ["nueva m I 5", "cargue m"]
        ch.compileLines(lines)
        declaration = ch.declaration
        self.assertEqual(5, declaration.getVariable('m'))
        self.assertTrue(type(declaration.getVariable('m')) is int)
        self.clearMemory()


    def testString(self):
        lines = ["nueva n C 5", "cargue n"]
        ch.compileLines(lines)
        declaration = ch.declaration
        self.assertEqual("5", declaration.getVariable('n'))
        self.assertTrue(type(declaration.getVariable('n')) is str)
        self.clearMemory()



    def testBool(self):
        lines = ["nueva o L 0", "cargue o"]
        ch.compileLines(lines)
        declaration = ch.declaration
        self.assertEqual(False, declaration.getVariable('o'))
        self.assertTrue(type(declaration.getVariable('o')) is bool)
        self.clearMemory()

    def testFloat(self):
        lines = ["nueva o R 2.5", "cargue o"]
        ch.compileLines(lines)
        declaration = ch.declaration
        self.assertEqual(2.5, declaration.getVariable('o'))
        self.assertTrue(type(declaration.getVariable('o')) is float)
        self.clearMemory()

if __name__ == '__main__':
    unittest.main()
