from ..errorHandling         import ErrorHandlerVariables
import time, requests, json, urllib.request

class ProgramDefinitions:
    def __init__(self , mem, variables, tags, runner=None):
        self.__mem       = variables.getMemory()
        self.__variables = variables
        self.__tags      = tags
        self.runner      = runner

    def cargar(self, name):
        if not self.__variables.inDeclarations(name):
            ErrorHandlerVariables.throw_var_no_declarada(name)
            return
        prev = self.__mem.getAcumulador()
        new  = self.__variables.getValue(name)

        self.__mem.setAcumulador(new)
        self.__mem.saveStepOneArg("Acumulador", prev, new)

    def almacene(self, name):  # * works
        if not self.__variables.inDeclarations(name):
            ErrorHandlerVariables.throw_var_no_declarada(name)
            exit()  # ! must send index to the end of the file
            return
        prev = self.__variables.getValue(name)
        new  = self.__mem.getAcumulador()
        self.__variables.setValue(name, new)
        self.__mem.saveStepOneArg(name, prev, new)

    def nueva(self, name, type_, value):  # !
        if self.__variables.inDeclarations(name):
            ErrorHandlerVariables.throw_var_ya_declarada(name)
            return
        value = self.check_type_and_cast(type_, value)
        self.__variables.setValue(name, value)
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

    def vaya(self,tag):
        if not self.__tags.inDeclarations(tag):
            ErrorHandlerVariables.throw_tag_no_declarada(tag)
            return
        self.runner.setLine(self.__tags.getValue(tag) -1)

    def vayasi(self, tag1, tag2):
        if not self.__tags.inDeclarations(tag1):
            ErrorHandlerVariables.throw_tag_no_declarada(tag1)
            exit()
            return
        if not self.__tags.inDeclarations(tag2):
            ErrorHandlerVariables.throw_tag_no_declarada(tag2)
            exit()
            return
        prev = self.runner.getCurrentLine()
        if self.__mem.getAcumulador() > 0:
            self.runner.setLine(self.__tags.getValue(tag1) -1) # makes it equal to the value in tag1
            self.__mem.saveStepOneArg("vayasi",str(" desde " + str(prev)+ " hasta "), self.runner.getCurrentLine())
            return
        if self.__mem.getAcumulador() < 0:
            self.runner.setLine(self.__tags.getValue(tag2)-1) # makes it equal to the value in tag2
            self.__mem.saveStepOneArg("vayasi", str(" desde " + str(prev)+ " hasta ") , self.runner.getCurrentLine())
            return
        self.__mem.saveStepOneArg("vayasi",str("desde " + str(prev)+ " hasta ") , self.runner.getCurrentLine())

    def etiqueta(self, name, value):
        if self.__tags.inDeclarations(name):
            ErrorHandlerVariables.throw_tag_ya_declarada(name)
            return
        try:
            value = int(value)
        except:
            ErrorHandlerVariables.throw_operando_no_es_numero()
            exit()
        self.__tags.setValue(name, value)
        self.__mem.saveStepOneArg(name, value)

    def lea(self, name):
        if not self.__variables.inDeclarations(name):
            ErrorHandlerVariables.throw_var_no_declarada(name)
            return

        # notifyApi = 'http://localhost:8000/api/leaCreateForm'
        # data = json.dumps({'createForm': True})
        # response = requests.post(notifyApi, data=data)
        # try:
        url_get = 'http://localhost:8000/api/lea'

        # try:
        response = requests.get(url_get, timeout=10)
        # except requests.exceptions.Timeout:
        #     print("Timeout occurred")
        # with urllib.request.urlopen(url_get) as url:
        #     s = url.read()
            # response = s.decode('utf8')
        prev  = self.__variables.getValue(name)
        var_type = self.__variables.getType(name)
        if(var_type == str):
            value = str(response.json()['lea'])
        if(var_type == bool):
            value = bool(response.json()['lea'])
        if(var_type == int):
            value = int(response.json()['lea'])
        if(var_type == float):
            value = float(response.json()['lea'])

        self.__variables.setValue(name, value)
        self.__mem.saveStepOneArg(name, prev, value)
        # while(True):
        #     if(response.json()['lea'] != None):
        #         break
        #     time.sleep(3)
        #     response = requests.get(url)


    def sume(self, name):
        if not self.__variables.inDeclarations(name):
            ErrorHandlerVariables.throw_var_no_declarada(name)
            return
        prev = self.__mem.getAcumulador()
        new  = self.__mem.getAcumulador() + self.__variables.getValue(name)

        self.__mem.setAcumulador(new)
        self.__mem.saveStepOneArg("Acumulador", prev, new)

    def reste(self, name):
        if not self.__variables.inDeclarations(name):
            ErrorHandlerVariables.throw_var_no_declarada(name)
            return
        prev = self.__mem.getAcumulador()
        new  = self.__mem.getAcumulador() - self.__variables.getValue(name)
        self.__mem.setAcumulador(new)
        self.__mem.saveStepOneArg("Acumulador", prev, new)

    def multiplique(self, name):
        if not self.__variables.inDeclarations(name):
            ErrorHandlerVariables.throw_var_no_declarada(name)
            return
        prev = self.__mem.getAcumulador()
        new = self.__mem.getAcumulador() * self.__variables.getValue(name)

        self.__mem.setAcumulador(new)
        self.__mem.saveStepOneArg("Acumulador", prev, new)

    def divida(self, name):
        if not self.__variables.inDeclarations(name):
            ErrorHandlerVariables.throw_var_no_declarada(name)
            return
        if self.__variables.getValue(name) == 0:
            ErrorHandlerVariables.throw_division_por_cero(
                self.__mem.getAcumulador(), self.__variables.getValue(name)
            )
            return
        
        prev = self.__mem.getAcumulador()
        new  = self.__mem.getAcumulador() / self.__variables.getValue(name)

        self.__mem.setAcumulador(new)
        self.__mem.saveStepOneArg("Acumulador", prev, new)

    def potencia(self, name):
        if not self.__variables.inDeclarations(name):
            ErrorHandlerVariables.throw_var_no_declarada(name)
            return
        prev = self.__mem.getAcumulador()
        new  = self.__mem.getAcumulador() ** self.__variables.getValue(name)

        self.__mem.setAcumulador(new)
        self.__mem.saveStepOneArg("Acumulador", prev, new)

    def modulo(self, name):
        if not self.__variables.inDeclarations(name):
            ErrorHandlerVariables.throw_var_no_declarada(name)
            return
        prev = self.__mem.getAcumulador()
        new  = self.__mem.getAcumulador() % self.__variables.getValue(name)

        self.__mem.setAcumulador(new)
        self.__mem.saveStepOneArg("Acumulador", prev, new)

    def concatene(self, name):  # ! variable value has to be a string
        if not self.__variables.inDeclarations(name):
            # if not a variable then is a normal string to concat
            self.__mem.setAcumulador(str(self.__mem.getAcumulador()) + name)
            return
        prev = self.__mem.getAcumulador()
        new = str(self.__mem.getAcumulador()) + self.__variables.getValue(name)

        self.__mem.setAcumulador(new)
        self.__mem.saveStepOneArg("Acumulador", prev, new)

    def elimine(self, to_delete, ans):
        if not self.__variables.inDeclarations(ans):
            ErrorHandlerVariables.throw_var_no_declarada(ans)
            return
        prev = self.__mem.getAcumulador()
        if not self.__variables.inDeclarations(to_delete):
            # if not a variable then is a normal string to concat
            substring = str(self.__mem.getAcumulador()).replace(to_delete, '')
            self.__variables.setValue(ans, substring)
            self.__mem.saveStepOneArg("Elimine",prev, substring)
            return

        to_delete = self.__variables.getValue(to_delete)
        substring = str(self.__mem.getAcumulador()).replace(to_delete, '')
        self.__variables.setValue(ans, substring)
        self.__mem.saveStepOneArg(ans, prev, substring)

    def extraiga(self, num_elem, ans):
        if not self.__variables.inDeclarations(ans):
            ErrorHandlerVariables.throw_var_no_declarada(ans)
            return
        prev = self.__mem.getAcumulador()

        substring = self.__mem.getAcumulador()[:int(num_elem)]
        self.__variables.setValue(ans, substring)
        self.__mem.saveStepOneArg(ans, prev, substring)

    def Y(self, first, second, ans):
        value = True if self.__variables.getValue(first) and self.__variables.getValue(second) else False
        self.__variables.setValue(ans, value)
        self.__mem.saveStepTwoArg("Y", first, second, value)

    def O(self, first, second, ans):
        value = True if self.__variables.getValue(first) or self.__variables.getValue(second) else False
        self.__variables.setValue(ans, value)
        self.__mem.saveStepTwoArg("O", first, second, value)

    def NO(self, first, ans):
        value = not self.__variables.getValue(first)
        self.__variables.setValue(ans, value)
        self.__mem.saveStepOneArg("NO", first, ans)

    def muestre(self, name):
        if(name == "acumulador"):
            self.runner.appendStdout(self.__mem.getAcumulador())
            return
        if not self.__variables.inDeclarations(name):
            ErrorHandlerVariables.throw_var_no_declarada(name)
            return
        value = self.__variables.getValue(name)
        self.runner.appendStdout(value)
        self.__mem.saveStepOneArg(name, value)

    def imprima(self):  # !!!!!!!!
        pass

    def max_(self, a, b, c):
        a = self.__variables.getValue(a)
        b = self.__variables.getValue(b)
        if(type(a) == str and type(b) == int):
            ErrorHandlerVariables.throw_operando_no_es_numero()
            return 
        if(type(a) == int and type(b) == str):
            ErrorHandlerVariables.throw_operando_no_es_numero()
            return 

        ans = a if a > b else b
        self.__variables.setValue(c, ans)

    def returne(self, value):
        self.__mem.saveStepOneArg("returne", value)
        return
