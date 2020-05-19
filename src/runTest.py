from chmaquina import Chmaquina
import os.path

def test():
    ch = Chmaquina()
    # ch.compileFile( os.path.dirname(__file__) + '/../programs/factorial.ch')
    ch.compileFile( os.path.dirname(__file__) + '/../programs/miProgTest.ch')
    ch.run_all()
    print(ch.getStdout())
    # print(ch.getVariables())
    # print(ch.getTags())
    # print(ch.getInstructionsReadable())
    # print(ch.getAcumulador())
    # print(ch.getSteps())

test()

#TODO make it work for any program uploaded