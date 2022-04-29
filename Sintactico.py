from prettytable import PrettyTable
from pyparsing import tokenMap
from Gestor import *
from ErrorS import ErrorS

class Sintactico:

    def __init__(self, tokens : list, gestor) -> None:
        self.errores = []
        self.columna = 0
        self.tokens = tokens
        self.gestor = gestor

    def agregarError(self, obtenido, esperado, columna):
        self.errores.append(ErrorS(obtenido, esperado,columna)) 

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
            self.agregarError("EOF","pr_RESULTADO | pr_JORNADA | pr_GOLES | pr_TABLA | pr_PARTIDOS | pr_TOP | pr_ADIOS", 0)
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
                self.agregarError("EOF","Cadena",0)
                return
            elif token.tipo == "Cadena":
                equipo1 = token.lexema
                token = self.popToken()
                if token is None:
                    self.agregarError("EOF","pr_VS",0)
                    return
                elif token.tipo == "pr_VS":
                    token = self.popToken()
                    if token is None:
                        self.agregarError("EOF","Cadena",0)
                        return
                    elif token.tipo == "Cadena":
                        equipo2 = token.lexema
                        token = self.popToken()
                        if token is None:
                            self.agregarError("EOF","pr_TEMPORADA",0)
                            return
                        elif token.tipo == "pr_TEMPORADA":
                            token = self.popToken()
                            if token is None:
                                self.agregarError("EOF","Menor que",0)
                                return
                            elif token.tipo == "Menor que":
                                token = self.popToken()
                                if token is None:
                                    self.agregarError("EOF","Entero",0)
                                    return
                                elif token.tipo == "Entero":
                                    año1 = token.lexema
                                    token = self.popToken()
                                    if token is None:
                                        self.agregarError("EOF","Guion",0)
                                        return
                                    elif token.tipo == "Guion":
                                        guion = token.lexema
                                        token = self.popToken()
                                        if token is None:
                                            self.agregarError("EOF","Entero",0)
                                            return
                                        elif token.tipo == "Entero":
                                            año2 = token.lexema
                                            token = self.popToken()
                                            if token is None:
                                                self.agregarError("EOF","Mayor que",0)
                                                return
                                            elif token.tipo == "Mayor que":
                                                fecha = str(año1)+str(guion)+str(año2)
                                                self.gestor.opResultado(equipo1,equipo2,fecha)
                                            else:
                                                self.agregarError(token.tipo,"Mayor que",0)
                                        else:
                                            self.agregarError(token.tipo,"Entero",0)
                                    else:
                                        self.agregarError(token.tipo,"Guion",0)
                                else:
                                    self.agregarError(token.tipo,"Entero",0)
                            else:
                                self.agregarError(token.tipo,"Menor que",0)
                        else:
                            self.agregarError(token.tipo,"pr_TEMPORADA",0)
                    else:
                        self.agregarError(token.tipo,"Cadena",0)
                else:
                    self.agregarError(token.tipo,"pr_VS",0)
            else:
                self.agregarError(token.tipo,"Cadena",0)
        else:
            self.agregarError("EOF","pr_RESULTADO",0)

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
                self.agregarError("EOF","Entero",0)
                return
            elif token.tipo == "Entero":
                jornada = token.lexema
                token = self.popToken()
                if token is None:
                    self.agregarError("EOF","pr_TEMPORADA",0)
                    return
                elif token.tipo == "pr_TEMPORADA":
                    token = self.popToken()
                    if token is None:
                        self.agregarError("EOF","Menor que",0)
                        return
                    elif token.tipo == "Menor que":
                        token = self.popToken()
                        if token is None:
                            self.agregarError("EOF","Entero",0)
                            return
                        elif token.tipo == "Entero":
                            año1 = token.lexema
                            token =self.popToken()
                            if token is None:
                                self.agregarError("EOF","Guion",0)
                                return
                            elif token.tipo == "Guion":
                                guion = token.lexema
                                token = self.popToken()
                                if token is None:
                                    self.agregarError("EOF","Entero",0)
                                    return
                                elif token.tipo == "Entero":
                                    año2 = token.lexema
                                    token = self.popToken()
                                    if token is None:
                                        self.agregarError("EOF","Mayor que", 0)
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
                                                self.agregarError("EOF","pr_f",0)
                                                return
                                            elif token.tipo == "pr_f":
                                                token = self.popToken()
                                                if token is None:
                                                    self.agregarError("EOF","String | Entero",0)
                                                    return
                                                elif token.tipo == "String" or token.tipo == "Entero":
                                                    nombre = token.lexema+".html"
                                                    fecha = str(año1)+str(guion)+str(año2)
                                                    self.gestor.opJornadaCon(jornada,fecha,nombre)
                                                else:
                                                    self.agregarError(token.tipo,"String | Entero",0)
                                            else:
                                                self.agregarError(token.tipo,"pr_f",0)
                                        else:
                                            self.agregarError(token.tipo,"Guion",0)
                                    else:
                                        self.agregarError(token.tipo,"Mayor que",0)
                                else:
                                    self.agregarError(token.tipo,"Entero",0)
                            else:
                                self.agregarError(token.tipo,"Guion",0)
                        else:
                            self.agregarError(token.tipo,"Entero",0)
                    else:
                        self.agregarError(token.tipo,"Menor que",0)
                else:
                    self.agregarError(token.tipo,"pr_TEMPORADA",0)
            else:
                self.agregarError(token.tipo,"Entero",0)
        else:
            self.agregarError("EOF","pr_JORNADA",0)

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
                self.agregarError("EOF","pr_LOCAL | pr_VISITANTE | pr_TOTAL",0)
                return
            elif token.tipo == "pr_LOCAL" or token.tipo == "pr_VISITANTE" or token.tipo == "pr_TOTAL":
                condicion = token.lexema
                token = self.popToken()
                if token is None:
                    self.agregarError("EOF","Cadena",0)
                    return
                elif token.tipo == "Cadena":
                    equipo = token.lexema
                    token = self.popToken()
                    if token is None:
                        self.agregarError("EOF","pr_TEMPORADA",0)
                        return
                    elif token.tipo == "pr_TEMPORADA":
                        token = self.popToken()
                        if token is None:
                            self.agregarError("EOF","Menor que",0)
                            return
                        elif token.tipo == "Menor que":
                            token = self.popToken()
                            if token is None:
                                self.agregarError("EOF","Entero",0)
                                return
                            elif token.tipo == "Entero":
                                año1 = token.lexema
                                token = self.popToken()
                                if token is None:
                                    self.agregarError("EOF","Guion",0)
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
                                            self.agregarError("EOF","Mayor que",0)
                                            return
                                        elif token.tipo == "Mayor que":
                                            fecha = str(año1)+str(guion)+str(año2)
                                            self.gestor.opGoles(condicion,equipo,fecha)
                                        else:
                                            self.agregarError(token.tipo,"Mayor que",0)
                                    else:
                                        self.agregarError(token.tipo,"Entero",0)
                                else:
                                    self.agregarError(token.tipo,"Guion",0)
                            else:
                                self.agregarError(token.tipo,"Entero",0)
                        else:
                            self.agregarError(token.tipo,"Menor que",0)
                    else:
                        self.agregarError(token.tipo,"pr_TEMPORADA",0)
                else:
                    self.agregarError(token.tipo,"Cadena",0)
            else:
                self.agregarError(token.tipo,"pr_LOCAL | pr_VISITANTE | pr_TOTAL",0)
        else:
            self.agregarError("EOF","pr_GOLES",0)

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
                self.agregarError("EOF","pr_TEMPORADA",0)
                return
            elif token.tipo == "pr_TEMPORADA":
                token = self.popToken()
                if token is None:
                    self.agregarError("EOF","Menor que",0)
                    return
                elif token.tipo == "Menor que":
                    token = self.popToken()
                    if token is None:
                        self.agregarError("EOF","Entero",0)
                        return
                    elif token.tipo == "Entero":
                        año1 = token.lexema
                        token = self.popToken()
                        if token is None:
                            self.agregarError("EOF","Guion",0)
                            return
                        elif token.tipo == "Guion":
                            guion = token.lexema
                            token = self.popToken()
                            if token is None:
                                self.agregarError("EOF","Entero",0)
                                return
                            elif token.tipo == "Entero":
                                año2 = token.lexema
                                token = self.popToken()
                                if token is None:
                                    self.agregarError("EOF","Mayor que",0)
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
                                            self.agregarError("EOF","pr_f",0)
                                            return
                                        elif token.tipo == "pr_f":
                                            token = self.popToken()
                                            if token is None:
                                                self.agregarError("EOF","String | Entero",0)
                                                return
                                            elif token.tipo == "String" or token.tipo == "Entero":
                                                nombre = token.lexema+".html"
                                                fecha = str(año1)+str(guion)+str(año2)
                                                self.gestor.opTablaCon(fecha,nombre)
                                            else:
                                                self.agregarError(token.tipo,"String | Entero",0)
                                        else:
                                            self.agregarError(token.tipo,"pr_f",0)
                                    else:
                                        self.agregarError(token.tipo,"Guion",0)
                                else:
                                    self.agregarError(token.tipo,"Mayor que",0)
                            else:
                                self.agregarError(token.tipo,"Entero",0)
                        else:
                            self.agregarError(token.tipo,"Guion",0)
                    else:
                        self.agregarError(token.tipo,"Entero",0)
                else:
                    self.agregarError(token.tipo,"Menor que",0)
            else:
                self.agregarError(token.tipo,"pr_TEMPORADA",0)
        else:
            self.agregarError("EOF","pr_TABLA",0)

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
                self.agregarError("EOF","Cadena",0)
                return
            elif token.tipo == "Cadena":
                equipo = token.lexema
                token = self.popToken()
                if token is None:
                    self.agregarError("EOF","pr_TEMPORADA",0)
                    return
                elif token.tipo == "pr_TEMPORADA":
                    token = self.popToken()
                    if token is None:
                        self.agregarError("EOF","Menor que",0)
                        return
                    elif token.tipo == "Menor que":
                        token = self.popToken()
                        if token is None:
                            self.agregarError("EOF","Entero",0)
                            return
                        elif token.tipo == "Entero":
                            año1 = token.lexema
                            token = self.popToken()
                            if token is None:
                                self.agregarError("EOF","Guion",0)
                                return
                            elif token.tipo == "Guion":
                                guion = token.lexema
                                token = self.popToken()
                                if token is None:
                                    self.agregarError("EOF","Entero",0)
                                    return
                                elif token.tipo == "Entero":
                                    año2 = token.lexema
                                    token = self.popToken()
                                    if token is None:
                                        self.agregarError("EOF","Mayor que",0)
                                        return
                                    elif token.tipo == "Mayor que":
                                        #token = self.popToken()
                                        fecha = str(año1)+str(guion)+str(año2)
                                        self.gestor.opPartidos(equipo,fecha,"","","")
                                    else:
                                        self.agregarError(token.tipo,"Mayor que",0)
                                else:
                                    self.agregarError(token.tipo,"Entero",0)
                            else:
                                self.agregarError(token.tipo,"Guion",0)
                        else:
                            self.agregarError(token.tipo,"Entero",0)
                    else:
                        self.agregarError(token.tipo,"Menor que",0)
                else:
                    self.agregarError(token.tipo,"pr_TEMPORADA",0)
            else:
                self.agregarError(token.tipo,"Cadena",0)
        else:
            self.agregarError("EOF","pr_PARTIDOS",0)

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
                self.agregarError("EOF","pr_SUPERIOR | pr_INFERIOR",0)
                return
            elif token.tipo == "pr_SUPERIOR" or token.tipo == "pr_INFERIOR":
                condicion = token.lexema
                token = self.popToken()
                if token is None:
                    self.agregarError("EOF","pr_TEMPORADA",0)
                    return
                elif token.tipo == "pr_TEMPORADA":
                    token = self.popToken()
                    if token is None:
                        self.agregarError("EOF","Menor que",0)
                        return
                    elif token.tipo == "Menor que":
                        token = self.popToken()
                        if token is None:
                            self.agregarError("EOF","Entero",0)
                            return
                        elif token.tipo == "Entero":
                            año1 = token.lexema
                            token = self.popToken()
                            if token is None:
                                self.agregarError("EOF","Guion",0)
                                return
                            elif token.tipo == "Guion":
                                guion = token.lexema
                                token = self.popToken()
                                if token is None:
                                    self.agregarError("EOF","Entero",0)
                                    return
                                elif token.tipo == "Entero":
                                    año2 = token.lexema
                                    token = self.popToken()
                                    if token is None:
                                        self.agregarError("EOF","Mayor que",0)
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
                                                self.agregarError("EOF","pr_n",0)
                                                return
                                            elif token.tipo == "pr_n":
                                                token = self.popToken()
                                                if token is None:
                                                    self.agregarError("EOF","Entero",0)
                                                    return
                                                elif token.tipo == "Entero":
                                                    top = token.lexema
                                                    fecha = str(año1)+str(guion)+str(año2)
                                                    self.gestor.opTopCon(condicion,fecha,top)
                                                else:
                                                    self.agregarError(token.tipo,"Entero",0)
                                            else:
                                                self.agregarError(token.tipo,"pr_n",0)
                                        else:
                                            self.agregarError(token.tipo,"Guion",0)
                                    else:
                                        self.agregarError(token.tipo,"Mayor que",0)
                                else:
                                    self.agregarError(token.tipo,"Entero",0)
                            else:
                                self.agregarError(token.tipo,"Guion",0)
                        else:
                            self.agregarError(token.tipo,"Entero",0)
                    else:
                        self.agregarError(token.tipo,"Menor que",0)
                else:
                    self.agregarError(token.tipo,"pr_TEMPORADA",0)
            else:
                self.agregarError(token.tipo,"pr_SUPERIOR | pr_INFERIOR",0)
        else:
            self.agregarError("EOF","pr_TOP",0)

    def ADIOS(self):
        token = self.popToken()
        if token.tipo == 'pr_ADIOS':
            self.gestor.opAdios()
        else:
            self.agregarError(token.tipo,'pr_ADIOS',0)
            
    def printErrorS(self):
        x = PrettyTable()
        x.field_names = ["ObtenidoS","EsperadoS","ColumnaS"]
        for error_ in self.errores:
            x.add_row([error_.obtenido,error_.esperado,error_.columna])
        print(x)
    
    def clearErroresS(self):
        self.errores.clear()