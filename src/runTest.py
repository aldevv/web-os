from chmaquina import Chmaquina
import os.path

def test():
    ch = Chmaquina()
    ch.compileFile( os.path.dirname(__file__) + '/../programs/printerTest.ch')
    ch.compileFile( os.path.dirname(__file__) + '/../programs/printerTest2.ch')
    ch.compileFile( os.path.dirname(__file__) + '/../programs/factorial.ch')
    # ch.compileFile( os.path.dirname(__file__) + '/../programs/testNueva.ch')
    ch.compileFile( os.path.dirname(__file__) + '/../programs/miProgTest.ch')
    # ch.compileFile( os.path.dirname(__file__) + '/../programs/testLea.ch')
    # ch.setAlgorithm("fifo")
    ch.setAlgorithm("priority")
    for instance in ch.scheduler.pending_run_instances:
        print(instance.progDefs.getDeclaration().getVariables())
    ch.run_all()
    print("stdout:", ch.getStdout())
    print("printer:", ch.getPrinter())
    ch.getSchedulerReport()
    # print(ch.getMemory())
    # print(ch.getVariables())
    # print(ch.getTags())
    # print(ch.getMemoryAvailable())
    # print(ch.getMemoryUsed())
    # print(ch.getPrograms())
    # print(ch.getRegisters())
    # print(ch.getAcumulador())
    # print(ch.getSteps()) 

test()
