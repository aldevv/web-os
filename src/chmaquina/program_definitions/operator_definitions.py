from ..errorHandling         import ErrorHandlerVariables
import time, requests, json, urllib.request

class OperatorDefinitions:
    def __init__(self , mem, declaration , runner):
        self.__mem         = mem
        self.__declaration = declaration
        self.runner        = runner
        self.lea_values    = None
        self.possible_operators = { 
                        "cargue":       self.cargar, 
                        "almacene":     self.almacene,
                        "vaya":         self.vaya, 
                        "vayasi":       self.vayasi,
                        "lea":          self.lea,
                        "sume":         self.sume,
                        "reste":        self.reste,
                        "multiplique":  self.multiplique,
                        "divida":       self.divida,
                        "potencia":     self.potencia,
                        "modulo":       self.modulo,
                        "concatene":    self.concatene,
                        "elimine":      self.elimine,
                        "extraiga":     self.extraiga,
                        "Y":            self.Y,
                        "O":            self.O,
                        "NO":           self.NO,
                        "muestre":      self.muestre,
                        "imprima":      self.imprima,
                        "max":          self.max_,
                        "returne":      self.returne
        }
    
    def get_possible_operators(self):
        return self.possible_operators
    
    def getDeclaration(self):
        return self.__declaration

    def cargar(self, name):
        if not self.__declaration.inDeclarations(name):
            ErrorHandlerVariables.throw_var_no_declarada(name)
            return
        prev = self.__mem.getAcumulador()
        new  = self.__declaration.getVariable(name)

        self.__mem.setAcumulador(new)
        self.__mem.saveStepOneArg("Acumulador", prev, new)

    def almacene(self, name):  # * works
        if not self.__declaration.inDeclarations(name):
            ErrorHandlerVariables.throw_var_no_declarada(name)
            exit()  # ! must send index to the end of the file
            return
        prev = self.__declaration.getVariable(name)
        new  = self.__mem.getAcumulador()
        self.__declaration.setVariable(name, new)
        self.__mem.saveStepOneArg(name, prev, new)

    def vaya(self,tag):
        if not self.__declaration.inDeclarations(tag):
            ErrorHandlerVariables.throw_tag_no_declarada(tag)
            return
        self.runner.setLine(self.__declaration.getTag(tag) -2)
        self.__mem.saveStepOneArg("vaya",str(" desde " + str(prev+1)+ " hasta "), self.runner.getCurrentLine()+1)

    def vayasi(self, tag1, tag2):
        if not self.__declaration.inDeclarations(tag1):
            ErrorHandlerVariables.throw_tag_no_declarada(tag1)
            exit()
            return
        if not self.__declaration.inDeclarations(tag2):
            ErrorHandlerVariables.throw_tag_no_declarada(tag2)
            exit()
            return
        prev = self.runner.getCurrentLine()
        if self.__mem.getAcumulador() > 0:
            self.runner.setLine(self.__declaration.getTag(tag1) -2) # makes it equal to the value in tag1
            self.__mem.saveStepOneArg("vayasi",str(" desde " + str(prev+1)+ " hasta "), self.runner.getCurrentLine()+1)
            return
        if self.__mem.getAcumulador() < 0:
            self.runner.setLine(self.__declaration.getTag(tag2)-2) # makes it equal to the value in tag2
            self.__mem.saveStepOneArg("vayasi", str(" desde " + str(prev+1)+ " hasta ") , self.runner.getCurrentLine()+1)
            return
        self.__mem.saveStepOneArg("vayasi",str("desde " + str(prev+1)+ " hasta ") , self.runner.getCurrentLine()+1)

    def lea(self, name):
        if not self.__declaration.inDeclarations(name):
            ErrorHandlerVariables.throw_var_no_declarada(name)
            return

        value = self.getValues(name)
        if value == None:
            return
        prev  = self.__declaration.getVariable(name)

        self.__declaration.setVariable(name, value)
        some  = self.__declaration.getVariable(name)
        self.__mem.saveStepOneArg(name, prev, value)

    def getValues(self, name):

        if self.lea_values == None:
            url_get = 'http://localhost:8000/api/lea'
            response = requests.get(url_get, timeout=10)
            self.lea_values = response.json()['lea']

        if self.lea_values == None:
            print("error obteniendo valores")
            return None

        value = self.lea_values.pop(0)
        var_type = self.__declaration.getVariableType(name)
        if(var_type == str):
            value = str(value)
        if(var_type == bool):
            value = bool(value)
        if(var_type == int):
            value = int(value)
        if(var_type == float):
            value = float(value)

        if len(self.lea_values) == 0:
            self.lea_values = None
        return value

    def sume(self, name):
        if not self.__declaration.inDeclarations(name):
            ErrorHandlerVariables.throw_var_no_declarada(name)
            return
        prev = self.__mem.getAcumulador()
        new  = self.__mem.getAcumulador() + self.__declaration.getVariable(name)

        self.__mem.setAcumulador(new)
        self.__mem.saveStepOneArg("Acumulador", prev, new)

    def reste(self, name):
        if not self.__declaration.inDeclarations(name):
            ErrorHandlerVariables.throw_var_no_declarada(name)
            return
        prev = self.__mem.getAcumulador()
        new  = self.__mem.getAcumulador() - self.__declaration.getVariable(name)
        self.__mem.setAcumulador(new)
        self.__mem.saveStepOneArg("Acumulador", prev, new)

    def multiplique(self, name):
        if not self.__declaration.inDeclarations(name):
            ErrorHandlerVariables.throw_var_no_declarada(name)
            return
        prev = self.__mem.getAcumulador()
        new = self.__mem.getAcumulador() * self.__declaration.getVariable(name)

        self.__mem.setAcumulador(new)
        self.__mem.saveStepOneArg("Acumulador", prev, new)

    def divida(self, name):
        if not self.__declaration.inDeclarations(name):
            ErrorHandlerVariables.throw_var_no_declarada(name)
            return
        if self.__declaration.getVariable(name) == 0:
            ErrorHandlerVariables.throw_division_por_cero(
                self.__mem.getAcumulador(), self.__declaration.getVariable(name)
            )
            return
        
        prev = self.__mem.getAcumulador()
        new  = self.__mem.getAcumulador() / self.__declaration.getVariable(name)

        self.__mem.setAcumulador(new)
        self.__mem.saveStepOneArg("Acumulador", prev, new)

    def potencia(self, name):
        if not self.__declaration.inDeclarations(name):
            ErrorHandlerVariables.throw_var_no_declarada(name)
            return
        prev = self.__mem.getAcumulador()
        new  = self.__mem.getAcumulador() ** self.__declaration.getVariable(name)

        self.__mem.setAcumulador(new)
        self.__mem.saveStepOneArg("Acumulador", prev, new)

    def modulo(self, name):
        if not self.__declaration.inDeclarations(name):
            ErrorHandlerVariables.throw_var_no_declarada(name)
            return
        prev = self.__mem.getAcumulador()
        new  = self.__mem.getAcumulador() % self.__declaration.getVariable(name)

        self.__mem.setAcumulador(new)
        self.__mem.saveStepOneArg("Acumulador", prev, new)

    def concatene(self, name):  # ! variable value has to be a string
        if not self.__declaration.inDeclarations(name):
            # if not a variable then is a normal string to concat
            self.__mem.setAcumulador(str(self.__mem.getAcumulador()) + name)
            return
        prev = self.__mem.getAcumulador()
        new = str(self.__mem.getAcumulador()) + self.__declaration.getVariable(name)

        self.__mem.setAcumulador(new)
        self.__mem.saveStepOneArg("Acumulador", prev, new)

    def elimine(self, to_delete, ans):
        if not self.__declaration.inDeclarations(ans):
            ErrorHandlerVariables.throw_var_no_declarada(ans)
            return
        prev = self.__mem.getAcumulador()
        if not self.__declaration.inDeclarations(to_delete):
            # if not a variable then is a normal string to concat
            substring = str(self.__mem.getAcumulador()).replace(to_delete, '')
            self.__declaration.setVariable(ans, substring)
            self.__mem.saveStepOneArg("Elimine",prev, substring)
            return

        to_delete = self.__declaration.getVariable(to_delete)
        substring = str(self.__mem.getAcumulador()).replace(to_delete, '')
        self.__declaration.setVariable(ans, substring)
        self.__mem.saveStepOneArg(ans, prev, substring)

    def extraiga(self, num_elem, ans):
        if not self.__declaration.inDeclarations(ans):
            ErrorHandlerVariables.throw_var_no_declarada(ans)
            return
        prev = self.__mem.getAcumulador()

        substring = self.__mem.getAcumulador()[:int(num_elem)]
        self.__declaration.setVariable(ans, substring)
        self.__mem.saveStepOneArg(ans, prev, substring)

    def Y(self, first, second, ans):
        value = True if self.__declaration.getVariable(first) and self.__declaration.getVariable(second) else False
        self.__declaration.setVariable(ans, value)
        self.__mem.saveStepTwoArg("Y", first, second, value)

    def O(self, first, second, ans):
        value = True if self.__declaration.getVariable(first) or self.__declaration.getVariable(second) else False
        self.__declaration.setVariable(ans, value)
        self.__mem.saveStepTwoArg("O", first, second, value)

    def NO(self, first, ans):
        value = not self.__declaration.getVariable(first)
        self.__declaration.setVariable(ans, value)
        self.__mem.saveStepOneArg("NO", first, ans)

    def muestre(self, name):
        if(name == "acumulador"):
            self.runner.appendStdout(self.__mem.getAcumulador())
            return
        if not self.__declaration.inDeclarations(name):
            ErrorHandlerVariables.throw_var_no_declarada(name)
            return
        value = self.__declaration.getVariable(name)
        self.runner.appendStdout(value)
        self.__mem.saveStepOneArg(name, value)

    def imprima(self, name):
        if(name == "acumulador"):
            self.runner.appendPrinter(self.__mem.getAcumulador())
            return
        if not self.__declaration.inDeclarations(name):
            ErrorHandlerVariables.throw_var_no_declarada(name)
            return
        value = self.__declaration.getVariable(name)
        self.runner.appendPrinter(value)
        self.__mem.saveStepOneArg(name, value)

    def max_(self, a, b, c):
        a = self.__declaration.getVariable(a)
        b = self.__declaration.getVariable(b)
        if(type(a) == str and type(b) == int):
            ErrorHandlerVariables.throw_operando_no_es_numero()
            return 
        if(type(a) == int and type(b) == str):
            ErrorHandlerVariables.throw_operando_no_es_numero()
            return 

        ans = a if a > b else b
        self.__declaration.setVariable(c, ans)

    def returne(self, value):
        self.__mem.saveStepOneArg("returne", value)
        return
