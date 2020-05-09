from chmaquina import Chmaquina

def test():
    ch = Chmaquina()
    ch.compileFile('programs/factorial.ch')
    ch.run_all()
    return ch.getStdin()

print(test())