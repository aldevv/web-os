from chmaquina import Chmaquina

import os.path

def test():
    #TODO change to dispatcher
    #put scheduler as container class, make dispatcher a 'has a' relationship
    #put declaration in the correct place, do this last because is a lot of work and sensitive changes
    #* put names in cpubursts and arrival times
    ch = Chmaquina()
    ch.compileFile( os.path.dirname(__file__) + '/../programs/printerTest.ch')
    ch.compileFile( os.path.dirname(__file__) + '/../programs/printerTest2.ch')
    ch.compileFile( os.path.dirname(__file__) + '/../programs/factorial.ch')
    # ch.compileFile( os.path.dirname(__file__) + '/../programs/testNueva.ch')
    ch.compileFile( os.path.dirname(__file__) + '/../programs/miProgTest.ch')
    # ch.compileFile( os.path.dirname(__file__) + '/../programs/testLea.ch')
    # ch.setAlgorithm("fifo")
    ch.setAlgorithm("priority")
    scheduler = ch.getScheduler()
    time = scheduler.getAlgorithm().getTime()
    print("start slice: ",time.getSlice())
    ch.run_all()
    time = scheduler.getAlgorithm().getTime()
    print("arrivals: ", time.getArrivalTimesHistory())
    print("cpuBursts: ", time.getCpuBurstsHistory())
    print("stdout:", ch.getStdout())
    print("printer:", ch.getPrinter())
    print("end slice: ",time.getSlice())
    scheduler.getSchedulerReport()
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
