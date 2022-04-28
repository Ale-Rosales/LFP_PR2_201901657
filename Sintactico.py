from prettytable import PrettyTable
from pyparsing import tokenMap
from Gestor import *

class Sintactico:

    def __init__(self, tokens : list, gestor) -> None:
        self.errores = []
        self.columna = 0
        self.tokens = tokens
        self.gestor = gestor

    def agregarError(self, esperado, obtenido, columna):
        self.errores.append("Error Sintactico: se obtuvo {} en la columna {}, se esperaba {}".format(obtenido, columna, esperado)) 

    def popToken(self):
        try:
            return self.tokens.pop(0)
        except:
            return None

    def viewToken(self):
        try:
            return self.tokens[0]
        except:
            return None

    def AnalizarS(self):
        self.S()

    def S(self):
        self.INICIO()

    def INICIO(self):
        temporal = self.viewToken()
        if temporal is None:
            self.agregarError("pr_RESULTADO | pr_JORNADA | pr_GOLES | pr_TABLA | pr_PARTIDOS | pr_TOP | pr_ADIOS", "EOF",0)
        elif temporal.tipo == 'pr_RESULTADO':
            self.RESULTADO()
        elif temporal.tipo == 'pr_JORNADA':
            self.JORNADA()
        elif temporal.tipo == 'pr_GOLES':
            self.GOLES()
        elif temporal.tipo == 'pr_TABLA':
            self.TABLA()
        elif temporal.tipo == 'pr_PARTIDOS':
            self.PARTIDOS()
        elif temporal.tipo == 'pr_TOP':
            self.TOP()
        elif temporal.tipo == 'pr_ADIOS':
            self.ADIOS()
    
    #FALTA ARREGLAR LAS COLUMNAS DE LOS ERRORES
    def RESULTADO(self):
        equipo1 = ""
        equipo2 = ""
        año1 = ""
        guion = ""
        año2 = ""
        fecha = ""
        token = self.popToken()
        if token.tipo == "pr_RESULTADO":
            token = self.popToken()
            if token is None:
                self.agregarError("Cadena","EOF",0)
                return
            elif token.tipo == "Cadena":
                equipo1 = token.lexema
                token = self.popToken()
                if token is None:
                    self.agregarError("pr_VS","EOF",0)
                    return
                elif token.tipo == "pr_VS":
                    token = self.popToken()
                    if token is None:
                        self.agregarError("Cadena","EOF",0)
                        return
                    elif token.tipo == "Cadena":
                        equipo2 = token.lexema
                        token = self.popToken()
                        if token is None:
                            self.agregarError("pr_TEMPORADA","EOF",0)
                            return
                        elif token.tipo == "pr_TEMPORADA":
                            token = self.popToken()
                            if token is None:
                                self.agregarError("Menor que","EOF",0)
                                return
                            elif token.tipo == "Menor que":
                                token = self.popToken()
                                if token is None:
                                    self.agregarError("Entero","EOF",0)
                                    return
                                elif token.tipo == "Entero":
                                    año1 = token.lexema
                                    token = self.popToken()
                                    if token is None:
                                        self.agregarError("Guion","EOF",0)
                                        return
                                    elif token.tipo == "Guion":
                                        guion = token.lexema
                                        token = self.popToken()
                                        if token is None:
                                            self.agregarError("Entero","EOF",0)
                                            return
                                        elif token.tipo == "Entero":
                                            año2 = token.lexema
                                            token = self.popToken()
                                            if token is None:
                                                self.agregarError("Mayor que","EOF",0)
                                                return
                                            elif token.tipo == "Mayor que":
                                                fecha = str(año1)+str(guion)+str(año2)
                                                self.gestor.opResultado(equipo1,equipo2,fecha)
                                            else:
                                                self.agregarError("Mayor que",token.tipo,0)
                                        else:
                                            self.agregarError("Entero",token.tipo,0)
                                    else:
                                        self.agregarError("Guion",token.tipo,0)
                                else:
                                    self.agregarError("Entero",token.tipo,0)
                            else:
                                self.agregarError("Menor que",token.tipo,0)
                        else:
                            self.agregarError("pr_TEMPORADA",token.tipo,0)
                    else:
                        self.agregarError("Cadena",token.tipo,0)
                else:
                    self.agregarError("pr_VS",token.tipo,0)
            else:
                self.agregarError("Cadena",token.tipo,0)
        else:
            self.agregarError("pr_RESULTADO","EOF",0)

    #VERIFICAR SI ESTA BIEN COMO SE HIZO SIN LISTA Y LAS COLUMNAS
    def JORNADA(self):
        jornada = ""
        año1 = ""
        guion = ""
        año2 = ""
        fecha = ""
        nombre = ""
        token = self.popToken()
        if token.tipo == "pr_JORNADA":
            token = self.popToken()
            if token is None:
                self.agregarError("Entero","EOF",0)
                return
            elif token.tipo == "Entero":
                jornada = token.lexema
                token = self.popToken()
                if token is None:
                    self.agregarError("pr_TEMPORADA","EOF",0)
                    return
                elif token.tipo == "pr_TEMPORADA":
                    token = self.popToken()
                    if token is None:
                        self.agregarError("Menor que","EOF",0)
                        return
                    elif token.tipo == "Menor que":
                        token = self.popToken()
                        if token is None:
                            self.agregarError("Entero","EOF",0)
                            return
                        elif token.tipo == "Entero":
                            año1 = token.lexema
                            token =self.popToken()
                            if token is None:
                                self.agregarError("Guion","EOF",0)
                                return
                            elif token.tipo == "Guion":
                                guion = token.lexema
                                token = self.popToken()
                                if token is None:
                                    self.agregarError("Entero","EOF",0)
                                    return
                                elif token.tipo == "Entero":
                                    año2 = token.lexema
                                    token = self.popToken()
                                    if token is None:
                                        self.agregarError("Mayor que", "EOF",0)
                                        return
                                    elif token.tipo == "Mayor que":
                                        token = self.popToken()
                                        if token is None:
                                            fecha = str(año1)+str(guion)+str(año2)
                                            nombre = "jornada_"+jornada+".html"
                                            self.gestor.opJornadaSin(jornada,fecha,nombre)
                                        elif token.tipo == "Guion":
                                            token = self.popToken()
                                            if token is None:
                                                self.agregarError("pr_f","EOF",0)
                                                return
                                            elif token.tipo == "pr_f":
                                                token = self.popToken()
                                                if token is None:
                                                    self.agregarError("String | Entero","EOF",0)
                                                    return
                                                elif token.tipo == "String" or token.tipo == "Entero":
                                                    nombre = token.lexema+".html"
                                                    fecha = str(año1)+str(guion)+str(año2)
                                                    self.gestor.opJornadaCon(jornada,fecha,nombre)
                                                else:
                                                    self.agregarError("String | Entero",token.tipo,0)
                                            else:
                                                self.agregarError("pr_f",token.tipo,0)
                                        else:
                                            self.agregarError("Guion",token.tipo,0)
                                    else:
                                        self.agregarError("Mayor que",token.tipo,0)
                                else:
                                    self.agregarError("Entero",token.tipo,0)
                            else:
                                self.agregarError("Guion",token.tipo,0)
                        else:
                            self.agregarError("Entero",token.tipo,0)
                    else:
                        self.agregarError("Menor que",token.tipo,0)
                else:
                    self.agregarError("pr_TEMPORADA",token.tipo,0)
            else:
                self.agregarError("Entero",token.tipo,0)
        else:
            self.agregarError("pr_JORNADA","EOF",0)

    #FALTA ARREGLAR LAS COLUMNAS DE LOS ERRORES
    def GOLES(self):
        equipo = ""
        año1 = ""
        guion = ""
        año2 = ""
        fecha = ""
        condicion = ""
        token = self.popToken()
        if token.tipo == "pr_GOLES":
            token = self.popToken()
            if token is None:
                self.agregarError("pr_LOCAL | pr_VISITANTE | pr_TOTAL","EOF",0)
                return
            elif token.tipo == "pr_LOCAL" or token.tipo == "pr_VISITANTE" or token.tipo == "pr_TOTAL":
                condicion = token.lexema
                token = self.popToken()
                if token is None:
                    self.agregarError("Cadena","EOF",0)
                    return
                elif token.tipo == "Cadena":
                    equipo = token.lexema
                    token = self.popToken()
                    if token is None:
                        self.agregarError("pr_TEMPORADA","EOF",0)
                        return
                    elif token.tipo == "pr_TEMPORADA":
                        token = self.popToken()
                        if token is None:
                            self.agregarError("Menor que","EOF",0)
                            return
                        elif token.tipo == "Menor que":
                            token = self.popToken()
                            if token is None:
                                self.agregarError("Entero","EOF",0)
                                return
                            elif token.tipo == "Entero":
                                año1 = token.lexema
                                token = self.popToken()
                                if token is None:
                                    self.agregarError("Guion","EOF",0)
                                    return
                                elif token.tipo == "Guion":
                                    guion = token.lexema
                                    token = self.popToken()
                                    if token is None:
                                        self.agregarError("Entero")
                                        return
                                    elif token.tipo == "Entero":
                                        año2 = token.lexema
                                        token = self.popToken()
                                        if token is None:
                                            self.agregarError("Mayor que","EOF",0)
                                            return
                                        elif token.tipo == "Mayor que":
                                            fecha = str(año1)+str(guion)+str(año2)
                                            self.gestor.opGoles(condicion,equipo,fecha)
                                        else:
                                            self.agregarError("Mayor que","EOF",0)
                                    else:
                                        self.agregarError("Entero",token.tipo,0)
                                else:
                                    self.agregarError("Guion",token.tipo,0)
                            else:
                                self.agregarError("Entero",token.tipo,0)
                        else:
                            self.agregarError("Menor que",token.tipo,0)
                    else:
                        self.agregarError("pr_TEMPORADA",token.tipo,0)
                else:
                    self.agregarError("Cadena",token.tipo,0)
            else:
                self.agregarError("pr_LOCAL | pr_VISITANTE | pr_TOTAL",token.tipo,0)
        else:
            self.agregarError("pr_GOLES","EOF",0)

    #VERIFICAR SI ESTA BIEN COMO SE HIZO SIN LISTA Y LAS COLUMNAS
    def TABLA(self):
        año1 = ""
        guion = ""
        año2 = ""
        fecha = ""
        token = self.popToken()
        if token.tipo == "pr_TABLA":
            token = self.popToken()
            if token is None:
                self.agregarError("pr_TEMPORADA","EOF",0)
                return
            elif token.tipo == "pr_TEMPORADA":
                token = self.popToken()
                if token is None:
                    self.agregarError("Menor que","EOF",0)
                    return
                elif token.tipo == "Menor que":
                    token = self.popToken()
                    if token is None:
                        self.agregarError("Entero","EOF",0)
                        return
                    elif token.tipo == "Entero":
                        año1 = token.lexema
                        token = self.popToken()
                        if token is None:
                            self.agregarError("Guion","EOF",0)
                            return
                        elif token.tipo == "Guion":
                            guion = token.lexema
                            token = self.popToken()
                            if token is None:
                                self.agregarError("Entero","EOF",0)
                                return
                            elif token.tipo == "Entero":
                                año2 = token.lexema
                                token = self.popToken()
                                if token is None:
                                    self.agregarError("Mayor que","EOF",0)
                                    return
                                elif token.tipo == "Mayor que":
                                    token = self.popToken()
                                    if token is None:
                                        fecha = str(año1)+str(guion)+str(año2)
                                        nombre = "temporada_"+str(fecha)+".html"
                                        self.gestor.opTablaSin(fecha,nombre)
                                    elif token.tipo == "Guion":
                                        token = self.popToken()
                                        if token is None:
                                            self.agregarError("pr_f","EOF",0)
                                            return
                                        elif token.tipo == "pr_f":
                                            token = self.popToken()
                                            if token is None:
                                                self.agregarError("String | Entero","EOF",0)
                                                return
                                            elif token.tipo == "String" or token.tipo == "Entero":
                                                nombre = token.lexema+".html"
                                                fecha = str(año1)+str(guion)+str(año2)
                                                self.gestor.opTablaCon(fecha,nombre)
                                            else:
                                                self.agregarError("String | Entero",token.tipo,0)
                                        else:
                                            self.agregarError("pr_f",token.tipo,0)
                                    else:
                                        self.agregarError("Guion",token.tipo,0)
                                    ####   AQUI IRIA LA LISTA
                                else:
                                    self.agregarError("Mayor que",token.tipo,0)
                            else:
                                self.agregarError("Entero",token.tipo,0)
                        else:
                            self.agregarError("Guion",token.tipo,0)
                    else:
                        self.agregarError("Entero",token.tipo,0)
                else:
                    self.agregarError("Menor que",token.tipo,0)
            else:
                self.agregarError("pr_TEMPORADA",token.tipo,0)
        else:
            self.agregarError("pr_TABLA","EOF",0)

    #VERIFICAR SI ESTA BIEN COMO SE HIZO SIN LISTA Y LAS COLUMNAS
    def PARTIDOS(self):
        equipo = ""
        año1 = ""
        guion = ""
        año2 = ""
        token = self.popToken()
        if token.tipo == "pr_PARTIDOS":
            token = self.popToken()
            if token is None:
                self.agregarError("Cadena","EOF",0)
                return
            elif token.tipo == "Cadena":
                equipo = token.lexema
                token = self.popToken()
                if token is None:
                    self.agregarError("pr_TEMPORADA","EOF",0)
                    return
                elif token.tipo == "pr_TEMPORADA":
                    token = self.popToken()
                    if token is None:
                        self.agregarError("Menor que","EOF",0)
                        return
                    elif token.tipo == "Menor que":
                        token = self.popToken()
                        if token is None:
                            self.agregarError("Entero","EOF",0)
                            return
                        elif token.tipo == "Entero":
                            año1 = token.lexema
                            token = self.popToken()
                            if token is None:
                                self.agregarError("Guion","EOF",0)
                                return
                            elif token.tipo == "Guion":
                                guion = token.lexema
                                token = self.popToken()
                                if token is None:
                                    self.agregarError("Entero","EOF",0)
                                    return
                                elif token.tipo == "Entero":
                                    año2 = token.lexema
                                    token = self.popToken()
                                    if token is None:
                                        self.agregarError("Mayor que","EOF",0)
                                        return
                                    elif token.tipo == "Mayor que":
                                        token = pow()
                                        ### AQUI VA LA LISTA
                                    else:
                                        self.agregarError("Mayor que",token.tipo,0)
                                else:
                                    self.agregarError("Entero",token.tipo,0)
                            else:
                                self.agregarError("Guion",token.tipo,0)
                        else:
                            self.agregarError("Entero",token.tipo,0)
                    else:
                        self.agregarError("Menor que",token.tipo,0)
                else:
                    self.agregarError("pr_TEMPORADA",token.tipo,0)
            else:
                self.agregarError("Cadena",token.tipo,0)
        else:
            self.agregarError("pr_PARTIDOS","EOF",0)

    #VERIFICAR SI ESTA BIEN COMO SE HIZO SIN LISTA Y LAS COLUMNAS
    def TOP(self):
        condicion = ""
        año1 = ""
        año2= ""
        guion = ""
        top = ""
        token = self.popToken()
        if token.tipo == "pr_TOP":
            token = self.popToken()
            if token is None:
                self.agregarError("pr_SUPERIOR | pr_INFERIOR","EOF",0)
                return
            elif token.tipo == "pr_SUPERIOR" or token.tipo == "pr_INFERIOR":
                condicion = token.lexema
                token = self.popToken()
                if token is None:
                    self.agregarError("pr_TEMPORADA","EOF",0)
                    return
                elif token.tipo == "pr_TEMPORADA":
                    token = self.popToken()
                    if token is None:
                        self.agregarError("Menor que","EOF",0)
                        return
                    elif token.tipo == "Menor que":
                        token = self.popToken()
                        if token is None:
                            self.agregarError("Entero","EOF",0)
                            return
                        elif token.tipo == "Entero":
                            año1 = token.lexema
                            token = self.popToken()
                            if token is None:
                                self.agregarError("Guion","EOF",0)
                                return
                            elif token.tipo == "Guion":
                                guion = token.lexema
                                token = self.popToken()
                                if token is None:
                                    self.agregarError("Entero","EOF",0)
                                    return
                                elif token.tipo == "Entero":
                                    año2 = token.lexema
                                    token = self.popToken()
                                    if token is None:
                                        self.agregarError("Mayor que","EOF",0)
                                        return
                                    elif token.tipo == "Mayor que":
                                        token = self.popToken()
                                        if token is None:
                                            fecha = str(año1)+str(guion)+str(año2)
                                            top = "5"
                                            self.gestor.opTopSin(condicion,fecha,top)
                                        elif token.tipo == "Guion":
                                            token = self.popToken()
                                            if token is None:
                                                self.agregarError("pr_n","EOF",0)
                                                return
                                            elif token.tipo == "pr_n":
                                                token = self.popToken()
                                                if token is None:
                                                    self.agregarError("Entero","EOF",0)
                                                    return
                                                elif token.tipo == "Entero":
                                                    top = token.lexema
                                                    fecha = str(año1)+str(guion)+str(año2)
                                                    self.gestor.opTopCon(condicion,fecha,top)
                                                else:
                                                    self.agregarError("Entero",token.tipo,0)
                                            else:
                                                self.agregarError("pr_n",token.tipo,0)
                                        else:
                                            self.agregarError("Guion",token.tipo,0)
                                    else:
                                        self.agregarError("Mayor que",token.tipo,0)
                                else:
                                    self.agregarError("Entero",token.tipo,0)
                            else:
                                self.agregarError("Guion",token.tipo,0)
                        else:
                            self.agregarError("Entero",token.tipo,0)
                    else:
                        self.agregarError("Menor que",token.tipo,0)
                else:
                    self.agregarError("pr_TEMPORADA",token.tipo,0)
            else:
                self.agregarError("pr_SUPERIOR | pr_INFERIOR",token.tipo,0)
        else:
            self.agregarError("pr_TOP","EOF",0)

    def ADIOS(self):
        token = self.popToken()
        if token.tipo == 'pr_ADIOS':
            self.gestor.opAdios()
        else:
            self.agregarError('pr_ADIOS',token.tipo,token.columna)
            
    def LISTA(self):
        #LISTA ::= BANDERA VALOR LISTA_
        bandera = self.BANDERA()
        if bandera is None:
            return
        
        lista_ = self.LISTA_()
        if lista_ is None:
            return
        return [bandera] + lista_
    
    def LISTA_(self):
        token = self.viewToken()
        if token is None:
            return
        bandera = self.BANDERA()
        if bandera is None:
            return
        lista_prima = self.LISTA_()
        if lista_prima is None:
            return
        return [bandera] + lista_prima
        
    def BANDERA(self):
        token = self.popToken()
        if token is None:
            self.agregarError("pr_f | pr_ji | pr_jf | pr_n","EOF",0)
            return
        if token.tipo == "pr_f":
            return token.lexema
        elif token.tipo == "pr_ji":
            return token.lexema
        elif token.tipo == "pr_jf":
            return token.lexema
        elif token.tipo == "pr_n":
            return token.lexema
        else:
            self.agregarError("pr_f | pr_ji | pr_jf | pr_n",token.tipo,0)
        valor = self.VALOR()
        if valor is None:
            return

    def VALOR(self):
        token = self.popToken()
        if token is None:
            self.agregarError("String | Entero","EOF",0)
            return
        if token.tipo == "String":
            return token.lexema
        elif token.tipo == "Entero":
            return int(token.lexema)
        else:
            self.agregarError("String | Entero", token.tipo,0)

    def ErroresS(self):
        x = PrettyTable()
        x.field_names = ["DescripcionS"]
        for error_ in self.errores:
            x.add_row([error_])
        print(x)
    
    def clearErroresS(self):
        self.errores.clear()