class ErrorHandlerVariables:
    @staticmethod
    def throw_var_no_declarada(name):
        print("error: variable ",name," no declarada")

    @staticmethod
    def throw_var_ya_declarada(name):
        print("error: variable ",name," ya declarada")

    @staticmethod
    def throw_tag_no_declarada(tag):
        print("etiqueta ",tag," no declarada")

    @staticmethod
    def throw_tag_ya_declarada(name):
        print("error: etiqueta ",name," ya declarada")

    @staticmethod
    def throw_operando_no_es_numero():
        print("no ingresaste un numeró en el operando")

    @staticmethod
    def throw_division_por_cero(acu, div):
        print("division por 0, entre ",acu, " y ",div)

    @staticmethod
    def throw_acu_not_string():
        print("error: acumulador no es un string")