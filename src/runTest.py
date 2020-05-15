from chmaquina import Chmaquina

def test():
    ch = Chmaquina()
    ch.compileFile('programs/factorial.ch')
    ch.run_all()
    print(ch.getStdout())
    print(ch.getVariables())
    print(ch.getTags())
    print(ch.getInstructions())
    print(ch.getAcumulador())
    print(ch.getSteps())

test()