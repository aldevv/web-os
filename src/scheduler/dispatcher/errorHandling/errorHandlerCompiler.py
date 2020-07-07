class ErrorHandlerCompiler:
    @staticmethod
    def throw_not_enough_memory_comp(compiler, dataStream, string):
        dataStream.appendError(compiler, str("not enough memory at compile time to enter instruction "+ str(" ".join(string))))

    @staticmethod
    def throw_too_many_arguments(compiler, dataStream, name, instruction):
        dataStream.appendError(compiler, str("Too many arguments: for function(declaration="+ str(name)+ " , instruction: "+ str(instruction)))

    @staticmethod
    def throw_not_enough_memory_runtime(compiler, dataStream, current_memory ):
        dataStream.appendError(compiler, str("not enough memory at run time (nothing ran), currentmemory" + str(current_memory)))