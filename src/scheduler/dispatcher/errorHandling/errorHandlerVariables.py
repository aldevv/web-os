class ErrorHandlerVariables: 
    @staticmethod
    def throw_var_no_declarada(runner, dataStream, name):
        dataStream.appendError(runner, str("error: variable "+name+" no declarada"))

    @staticmethod
    def throw_var_ya_declarada(runner, dataStream, name):
        dataStream.appendError(runner, str("error: variable "+name+" ya declarada"))

    @staticmethod
    def throw_tag_no_declarada(runner, dataStream, tag):
        dataStream.appendError(runner, str("etiqueta "+tag+" no declarada"))

    @staticmethod
    def throw_tag_ya_declarada(runner, dataStream, name):
        dataStream.appendError(runner, str("error: etiqueta "+name+" ya declarada"))

    @staticmethod
    def throw_operando_no_es_numero(runner, dataStream, val):
        dataStream.appendError(runner, str("no ingresaste un numeró en el operando" + str(val)))

    @staticmethod
    def throw_tipo_no_valido(runner, dataStream, tipo):
        dataStream.appendError(runner, str("no ingresaste tipo de dato valido " + str(tipo)))

    @staticmethod
    def throw_division_por_cero(runner, dataStream, acu, div):
        dataStream.appendError(runner, str("division por 0, entre "+str(acu)+ " y "+ str(div)))
    
    @staticmethod
    def try_error(runner, dataStream, message):
        dataStream.appendError(runner, message)

    def funcion_no_definida(runner, dataStream, message):
        dataStream.appendError(runner, message)
