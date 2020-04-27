class ErrorHandlerVariables:
    def throw_var_no_declarada(self, name):
        print("error: variable ",name," no declarada")
    def throw_var_ya_declarada(self, name):
        print("error: variable ",name," ya declarada")
    def throw_tag_no_declarada(self, tag):
        print("etiqueta ",tag," no declarada")
    def throw_tag_ya_declarada(self, name):
        print("error: etiqueta ",name," ya declarada")
    def throw_operando_no_es_numero(self):
        print("no ingresaste un numeró en el operando")
    def throw_division_por_cero(self, acu, div):
        print("division por 0, entre ",acu, " y ",div)
    def throw_acu_not_string(self):
        print("error: acumulador no es un string")