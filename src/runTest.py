from chmaquina import Chmaquina

def test():
    ch = Chmaquina()
    ch.compileFile('programs/factorial.ch')
    ch.run_all()
    print(ch.getStdin())
    print(ch.getVariables())
    print(ch.getTags())
    print(ch.getInstructions())
    print(ch.getAcumulador())

test()