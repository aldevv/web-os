class ErrorHandlerCompiler:

    def throw_not_enough_memory_comp(self, string):
        print("not enough memory at compile time to enter instruction "," ".join(string))

    def throw_too_many_arguments(self):
        print("Too many arguments")

    def throw_not_enough_memory_runtime(self):
        print("not enough memory at run time (nothing ran)")