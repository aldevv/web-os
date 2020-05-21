from chmaquina import Chmaquina
import os.path

def test():
    ch = Chmaquina()
    ch.compileFile( os.path.dirname(__file__) + '/../programs/factorial.ch')
    # ch.compileFile( os.path.dirname(__file__) + '/../programs/miProgTest.ch')
    # ch.compileFile( os.path.dirname(__file__) + '/../programs/testLea.ch')
    ch.run_all()
    print(ch.getStdout())
    print(ch.getMemoryAvailable())
    print(ch.getMemoryUsed())
    # print(ch.getPrograms())
    # print(ch.getVariablesHistory())
    # print(ch.getTagsHistory())
    print(ch.getRegisters())
    # print(ch.getAcumulador())
    # print(ch.getSteps())

test()

#TODO make it work for any program uploaded