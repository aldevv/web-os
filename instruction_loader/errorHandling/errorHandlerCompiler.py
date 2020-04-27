class ErrorHandlerCompiler:
    @staticmethod
    def throw_not_enough_memory_comp(string):
        print("not enough memory at compile time to enter instruction "," ".join(string))

    @staticmethod
    def throw_too_many_arguments(name, instruction, declaration_state):
        print("Too many arguments: for function(declaration=",declaration_state,"): ", name, " , instruction: ", instruction)

    @staticmethod
    def throw_not_enough_memory_runtime():
        print("not enough memory at run time (nothing ran)")