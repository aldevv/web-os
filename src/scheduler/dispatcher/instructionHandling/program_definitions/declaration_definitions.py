from ...errorHandling         import ErrorHandlerVariables

class DeclarationDefinitions:
    def __init__(self , mem, declaration):
        self.__mem         = mem
        self.__declaration = declaration
        self.possible_declarations = {
                        "nueva":self.nueva,
                        "etiqueta":self.etiqueta,
        }

    def getDeclaration(self):
        return self.__declaration
    
    def get_possible_declarations(self):
        return self.possible_declarations

    def nueva(self, name, type_, value=None): 
        if self.__declaration.inDeclarations(name):
            ErrorHandlerVariables.throw_var_ya_declarada(name)
            return
        if value == None:
            value = 0

        value = self.check_type_and_cast(type_, value)
        self.__declaration.setVariable(name, value)
        self.__mem.saveStepOneArg(name, value)

    def check_type_and_cast(self, type_, value):
        try:
            if(type_ == "C"):
                value = str(value)
            if(type_ == "I"):
                value = int(value)
            if(type_ == "R"):
                value = float(value)
            if(type_ == "L"):
                value = int(value)
                value = bool(value)
            return value
        except TypeError:
            ErrorHandlerVariables.throw_operando_no_es_numero()
            exit()

    def etiqueta(self, name, value):
        if self.__declaration.inDeclarations(name):
            ErrorHandlerVariables.throw_tag_ya_declarada(name)
            return
        try:
            value = int(value)
        except:
            ErrorHandlerVariables.throw_operando_no_es_numero()
            exit()
        self.__declaration.setTag(name, value)
        self.__mem.saveStepOneArg(name, value)