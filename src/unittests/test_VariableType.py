import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from scheduler import Scheduler
import unittest

ch = Scheduler()
mem = ch.dispatcher.mem
class VariableTypeTest(unittest.TestCase):

    def testInt(self):
        lines = ["nueva m I 5", "cargue m"]
        ch.compileLines(lines)
        declaration = ch.getDeclaration()
        self.assertEqual(5, declaration.getVariable('m'))
        self.assertTrue(type(declaration.getVariable('m')) is int)
        ch.resetMaquina()


    def testString(self):
        lines = ["nueva n C 5", "cargue n"]
        ch.compileLines(lines)
        declaration = ch.getDeclaration()
        self.assertEqual("5", declaration.getVariable('n'))
        self.assertTrue(type(declaration.getVariable('n')) is str)
        ch.resetMaquina()



    def testBool(self):
        lines = ["nueva o L 0", "cargue o"]
        ch.compileLines(lines)
        declaration = ch.getDeclaration()
        self.assertEqual(False, declaration.getVariable('o'))
        self.assertTrue(type(declaration.getVariable('o')) is bool)
        ch.resetMaquina()

    def testFloat(self):
        lines = ["nueva o R 2.5", "cargue o"]
        ch.compileLines(lines)
        declaration = ch.getDeclaration()
        self.assertEqual(2.5, declaration.getVariable('o'))
        self.assertTrue(type(declaration.getVariable('o')) is float)
        ch.resetMaquina()

if __name__ == '__main__':
    unittest.main()
