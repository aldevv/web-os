from .errorHandlerVariables import ErrorHandlerVariables


class Program:
    def __init__(self, Memory):
        self.__mem = Memory
        self.__e = ErrorHandlerVariables()

    def cargar(self, name):
        if not self.__mem.inDeclarations(name):
            self.__e.throw_var_no_declarada(name)
            return
        self.__mem.setAcumulador(self.__mem.getVariable(name))

    def almacene(self, name):  # * works
        if not self.__mem.inDeclarations(name):
            self.__e.throw_var_no_declarada(name)
            exit()  # ! must send index to the end of the file
            return
        self.__mem.setVariable(name, self.__mem.getAcumulador())

    def nueva(self, name, type_, value):  # !
        if self.__mem.inDeclarations(name):
            self.__e.throw_var_ya_declarada(name)
            return
        value = self.check_type(type_, value)
        self.__mem.setVariable(name, value)

    def check_type(self, type_, value):
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
            self.__e.throw_operando_no_es_numero()
            exit()

    def etiqueta(self, name, value):
        if self.__mem.inDeclarations(name):
            self.__e.throw_tag_ya_declarada(name)
            return
        try:
            value = int(value)
        except:
            self.__e.throw_operando_no_es_numero()
            exit()
        self.__mem.setVariable(name, value, tag=True)

    def lea(self, name):
        if not self.__mem.inDeclarations(name):
            self.__e.throw_var_no_declarada(name)
            return
        value = int(input("ingrese valor"))
        self.__mem.variables.all_data[name] = value
        
        # self.__mem.setVariable(name, value)

    def sume(self, name):
        if not self.__mem.inDeclarations(name):
            self.__e.throw_var_no_declarada(name)
            return
        self.__mem.setAcumulador(
            self.__mem.getAcumulador() + self.__mem.getVariable(name))

    def reste(self, name):
        if not self.__mem.inDeclarations(name):
            self.__e.throw_var_no_declarada(name)
            return
        self.__mem.setAcumulador(
            self.__mem.getAcumulador() - self.__mem.getVariable(name))

    def multiplique(self, name):
        if not self.__mem.inDeclarations(name):
            self.__e.throw_var_no_declarada(name)
            return
        self.__mem.setAcumulador(
            self.__mem.getAcumulador() * self.__mem.getVariable(name))

    def divida(self, name):
        if not self.__mem.inDeclarations(name):
            self.__e.throw_var_no_declarada(name)
            return
        if self.__mem.getVariable(name) == 0:
            self.__e.throw_division_por_cero(
                self.__mem.getAcumulador(), self.__mem.getVariable(name))
            return
        self.__mem.setAcumulador(
            self.__mem.getAcumulador() / self.__mem.getVariable(name))

    def potencia(self, name):
        if not self.__mem.inDeclarations(name):
            self.__e.throw_var_no_declarada(name)
            return
        self.__mem.setAcumulador(
            self.__mem.getAcumulador() ** self.__mem.getVariable(name))

    def modulo(self, name):
        if not self.__mem.inDeclarations(name):
            self.__e.throw_var_no_declarada(name)
            return
        self.__mem.setAcumulador(self.__mem.getAcumulador() %
                                 self.__mem.getVariable(name))

    def concatene(self, name):  # ! variable value has to be a string
        if not self.__mem.inDeclarations(name):
            # if not a variable then is a normal string to concat
            self.__mem.setAcumulador(str(self.__mem.getAcumulador()) + name)
            return
        self.__mem.setAcumulador(
            str(self.__mem.getAcumulador()) + self.__mem.getVariable(name))

    def elimine(self, to_delete):
        if type(self.__mem.getAcumulador()) != str:
            self.__e.throw_acu_not_string()
            return
        subcadena = self.__mem.getAcumulador().strip(to_delete)

    def extraiga(self, substr):
        subcadena = self.__mem.getAcumulador()[:substr]

    def Y(self, first, second, ans):
        self.__mem.setVariable(ans, True if self.__mem.getVariable(
            first) and self.__mem.getVariable(second) else False)

    def O(self, first, second, ans):
        self.__mem.setVariable(ans, True if self.__mem.getVariable(
            first) or self.__mem.getVariable(second) else False)

    def NO(self, first, ans):
        self.__mem.setVariable(ans, not self.__mem.getVariable(first))

    def muestre(self, name):
        if(name == "acumulador"):
            print(self.__mem.getAcumulador())
            return
        if not self.__mem.inDeclarations(name):
            self.__e.throw_var_no_declarada(name)
            return
        print(self.__mem.getVariable(name))

    def imprima(self):  # !!!!!!!!
        pass

    def max_(self, a, b):
        if(type(a) == str and type(b) == str):
            return self.__mem.getVariable(a) if self.__mem.getVariable(a) > self.__mem.getVariable(b) else self.__mem.getVariable(b)
        if(type(a) == str and b == int):
            return self.__mem.getVariable(a) if self.__mem.getVariable(a) > b else b
        if(a == int and type(b) == str):
            return a if a > self.__mem.getVariable(b) else self.__mem.getVariable(b)
        return a if a > b else b

    def returne(self, value):
        return
