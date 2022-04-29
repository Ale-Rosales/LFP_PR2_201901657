
from pyparsing import TokenConverter
from Data import Data
import easygui
import re
from tkinter import messagebox as MessageBox
import sys
import random
import os
import webbrowser

from Tabla import Tabla

texto = ""

class Gestor:

    def __init__(self):
        self.data = []
        self.aux = []
        self.puntos = []

    def crearData(self,fecha,temporada,jornada,equipo1,equipo2,goles1,goles2):
        self.data.append(Data(fecha,temporada,jornada,equipo1,equipo2,goles1,goles2))
    
    def tablaE(self,equipo,puntos):
        self.puntos.append(Tabla(equipo,puntos))

    def cargarData(self):
        archivo = open("LaLigaBot-LFP.csv",'r', encoding = "utf-8")
        contenido = archivo.read()
        archivo.close()
        try:
            aux = re.split('\n',contenido)
            i = 1
            while i < len(aux):
                data = re.split(',',aux[i])
                self.crearData(data[0],data[1],data[2],data[3],data[4],int(data[5]),int(data[6]))
                i = i+1
        except Exception as e:
            print(e)

    #PARA VERIFICAR QUE SI ESTA LA DATA CARGADA
    def Print(self):
        for x in self.data:
            print(x.equipo1)


    def opResultado(self,equipo1,equipo2,fecha):
        global texto
        eq1 = equipo1.replace('"','')
        eq2 = equipo2.replace('"','')
        #print(cadena1+"\n"+cadena2+"\n"+fecha)
        #print("\n")
        try:
            for x in self.data:
                if x.temporada == fecha and x.equipo1 == eq1 and x.equipo2 == eq2:
                    texto = "El resultado de este partido fue: "+x.equipo1+": "+str(x.goles1)+" - "+x.equipo2+": "+str(x.goles2)
        except:
            MessageBox.showwarning("Alerta", "Parece que ocurrio un error.")


    def opGoles(self,condicion,equipo,fecha):
        global texto
        eq = equipo.replace('"','')
        t_goles = 0
        t_gL = 0
        t_gV = 0
        #print(condicion+"\n"+eq+"\n"+fecha)
        if condicion == "LOCAL":
            for x in self.data:
                if x.temporada == fecha and x.equipo1 == eq:
                    #print("SI ENTRA AL IF")
                    t_goles += x.goles1
            #print(t_goles)
            texto = "Los goles anotados por el "+eq+" en total en la temporada "+fecha+"fueron "+str(t_goles)
        elif condicion == "VISITANTE":
            for x in self.data:
                if x.temporada == fecha and x.equipo2 == eq:
                    #print("SI ENTRA AL IF")
                    t_goles += x.goles2
            #print(t_goles)
            texto = "Los goles anotados por el "+eq+" en total en la temporada "+fecha+"fueron "+str(t_goles)
        elif condicion == "TOTAL":
            for x in self.data:
                if x.temporada == fecha and x.equipo1 == eq:
                    t_gL += x.goles1
                if x.temporada == fecha and x.equipo2 == eq:
                    t_gV += x.goles2
            #print("Local: "+str(t_gL))
            #print("Visitante: "+str(t_gV))
            t_goles = t_gL + t_gV
            #print("Totales: "+str(t_goles))
            texto = "Los goles anotados por el "+eq+" en total en la temporada "+fecha+"fueron "+str(t_goles)
                

    def opJornadaSin(self,jornada,fecha,nombre):
        global texto
        texto = "Archivo de resultados jornada "+str(jornada)+" temporada "+str(fecha)+" generado."
        textoTabla = ""
        txtFinal = ('</div>'
            '</body>'
            '</html>')
        
        i = 0
        for x in self.data:
            if x.jornada == jornada and x.temporada == fecha:
                i += 1
                textoTabla = textoTabla+'<tr>'+'<td>'+str(x.equipo1)+'</td>'+'<td>'+str(x.equipo2)+'</td>'+'<td>'+str(x.goles1)+" - "+str(x.goles2)+'</td>'+'</tr>'
                #print(x.equipo1+": "+str(x.goles1)+" - "+x.equipo2+": "+str(x.goles2))

        contenidoHTML = (
            '<!DOCTYPE html>'
            '<html>' 
            '<head> '
            '<meta charset="utf-8"> '
            '<title>REPORTE JORNADA '+str(jornada)+'</title>'
            '<link href="assets/css/bootstrap-responsive.css" type="text/css" rel="stylesheet">'
            '<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css" type="text/css" rel="stylesheet">'
            '<link rel="stylesheet" type="text/css"  href="Style.css">'
            '<link rel="stylesheet" type="text/css" href="bootstrap.css">'
            '</head>'
            '<body>'
            '<div class="container-fluid welcome-page" id="home">'
            '<div class="jumbotron">'
            '<h1>'
            '<span>'+"Jornada "+str(jornada)+" Temporada "+str(fecha)+'</span>'
            '</h1>'
            '</div>'
            '</div>')
        
        file = open("./REPORTES/"+nombre,"w",encoding = "utf-8")
        file.write(str(contenidoHTML))
        file.write('<h2>'
            '<span>Resumen de jornada/temporada</span>'
            '</h2>'
            '</br>'
            '</br>')
        
        txtHtml=(
            '<table class="table table-responsive">'
            '<thead>'
            '<tr>'
            '<th scope="col">Equipo Local</th>'
            '<th scope="col">Equipo Visitante</th>'
            '<th scope="col">Resultado</th>'
            '</tr>'
            '</thead>'
            '<tbody>')
        
        for x in self.data:
            if x.jornada == jornada and x.temporada == fecha:
                i += 1
                txtHtml = txtHtml+'<tr>'+'<td>'+str(x.equipo1)+'</td>'+'<td>'+str(x.equipo2)+'</td>'+'<td>'+str(x.goles1)+" - "+str(x.goles2)+'</td>'+'</tr>'
        
        file.write(txtHtml)
        file.write('</tbody>'
            '</table>'
            '</div>'
            '</div>')
 
        file.write(txtFinal)
        file.close()
        webbrowser.open("file:///"+os.getcwd()+"/REPORTES/"+nombre)
        #print(jornada+"\n"+fecha+"\n"+nombre)


    def opJornadaCon(self,jornada,fecha,nombre):
        global texto
        texto = "Archivo de resultados jornada "+str(jornada)+" temporada "+str(fecha)+" generado."
        textoTabla = ""
        txtFinal = ('</div>'
            '</body>'
            '</html>')
        
        i = 0
        for x in self.data:
            if x.jornada == jornada and x.temporada == fecha:
                i += 1
                textoTabla = textoTabla+'<tr>'+'<td>'+str(x.equipo1)+'</td>'+'<td>'+str(x.equipo2)+'</td>'+'<td>'+str(x.goles1)+" - "+str(x.goles2)+'</td>'+'</tr>'
                #print(x.equipo1+": "+str(x.goles1)+" - "+x.equipo2+": "+str(x.goles2))

        contenidoHTML = (
            '<!DOCTYPE html>'
            '<html>' 
            '<head> '
            '<meta charset="utf-8"> '
            '<title>REPORTE JORNADA '+str(jornada)+'</title>'
            '<link href="assets/css/bootstrap-responsive.css" type="text/css" rel="stylesheet">'
            '<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css" type="text/css" rel="stylesheet">'
            '<link rel="stylesheet" type="text/css"  href="Style.css">'
            '<link rel="stylesheet" type="text/css" href="bootstrap.css">'
            '</head>'
            '<body>'
            '<div class="container-fluid welcome-page" id="home">'
            '<div class="jumbotron">'
            '<h2>'
            '<span>'+"Jornada "+str(jornada)+" Temporada "+str(fecha)+'</span>'
            '</h2>'
            '</div>'
            '</div>')
        
        file = open("./REPORTES/"+nombre,"w",encoding = "utf-8")
        file.write(str(contenidoHTML))
        file.write('<h2>'
            '<span>Resumen de jornada/temporada</span>'
            '</h2>'
            '</br>'
            '</br>')
        
        txtHtml=(
            '<table class="table table-responsive">'
            '<thead>'
            '<tr>'
            '<th scope="col">Equipo Local</th>'
            '<th scope="col">Equipo Visitante</th>'
            '<th scope="col">Resultado</th>'
            '</tr>'
            '</thead>'
            '<tbody>')
        
        for x in self.data:
            if x.jornada == jornada and x.temporada == fecha:
                i += 1
                txtHtml = txtHtml+'<tr>'+'<td>'+str(x.equipo1)+'</td>'+'<td>'+str(x.equipo2)+'</td>'+'<td>'+str(x.goles1)+" - "+str(x.goles2)+'</td>'+'</tr>'
        
        file.write(txtHtml)
        file.write('</tbody>'
            '</table>'
            '</div>'
            '</div>')

        file.write(txtFinal)
        file.close()
        webbrowser.open("file:///"+os.getcwd()+"/REPORTES/"+nombre)
        #print(jornada+"\n"+fecha+"\n"+nombre)
    
    def opTablaSin(self,fecha,nombre):
        # VICTORIA SUMA 3 PUNTOS
        # EMPATE SUMA 1 PUNTOS
        # DERROTA SUMA 0 PUNTOS
        listEq1 = dict()
        listEq2 = dict()
        aux1 = []
        aux2 = []
        equipos = []
        cont = 0
        cont2 = 0
        #AGREGAR A DICCIONARIOS LOS EQUIPOS EN LA TEMPORADA
        for x in self.data:
            if x.temporada == fecha:
                if x.equipo1 in listEq1:
                    if listEq1[x.equipo1] == 1:
                        cont  =+ 1
                    listEq1[x.equipo1] += 1
                else:
                    listEq1[x.equipo1] = 1

                if x.equipo2 in listEq2:
                    if listEq2[x.equipo2] == 1:
                        cont2 =+ 1
                    listEq2[x.equipo2] += 1
                else:
                    listEq2[x.equipo2] = 1
        #AGREGAR LAS LLAVES DEL DICCIONARIO A LISTA
        for x in listEq1:
            aux1.append(x)
        for y in listEq2:
            aux2.append(y)   
        #AGREGAR A UNA LISTA LOS EQUIPOS IGUALES EN CADA DICCIONARIO
        for e in aux1:
            for f in aux2:
                if(e==f):
                    equipos.append(e)
                    break

        global texto
        texto = "Archivo de clasificacion de temporada "+str(fecha)+" generado."
        textoTabla = ""
        txtFinal = ('</div>'
            '</body>'
            '</html>')
        
        i = 0
        for x in equipos:
            i += 1
            textoTabla = textoTabla+'<tr>'+'<td>'+str(x)+'</td>'+'<td></td>'+'</tr>'
        
        contenidoHTML = (
            '<!DOCTYPE html>'
            '<html>' 
            '<head> '
            '<meta charset="utf-8"> '
            '<title>REPORTE CLASIFICACION '+str(fecha)+'</title>'
            '<link href="assets/css/bootstrap-responsive.css" type="text/css" rel="stylesheet">'
            '<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css" type="text/css" rel="stylesheet">'
            '<link rel="stylesheet" type="text/css"  href="Style.css">'
            '<link rel="stylesheet" type="text/css" href="bootstrap.css">'
            '</head>'
            '<body>'
            '<div class="container-fluid welcome-page" id="home">'
            '<div class="jumbotron">'
            '<h2>'
            '<span>'+"Clasificacion Temporada "+str(fecha)+'</span>'
            '</h2>'
            '</div>'
            '</div>')
        
        file = open("./REPORTES/"+nombre,"w",encoding = "utf-8")
        file.write(str(contenidoHTML))
        file.write('<h2>'
            '<span>Resumen de clasificacion</span>'
            '</h2>'
            '</br>'
            '</br>')
        
        txtHtml=(
            '<table class="table table-responsive">'
            '<thead>'
            '<tr>'
            '<th scope="col">Equipo</th>'
            '<th scope="col">Puntos</th>'
            '</tr>'
            '</thead>'
            '<tbody>')
        
        for x in equipos:
            i += 1
            txtHtml = txtHtml+'<tr>'+'<td>'+str(x)+'</td>'+'<td></td>'+'</tr>'
        
        file.write(txtHtml)
        file.write('</tbody>'
            '</table>'
            '</div>'
            '</div>')

        file.write(txtFinal)
        file.close()
        webbrowser.open("file:///"+os.getcwd()+"/REPORTES/"+nombre)

        #print(equipos)
        #print("Cantidad de Equipos en la Temporada: "+str(len(equipos)))
    
    def opTablaCon(self,fecha,nombre):
        # VICTORIA SUMA 3 PUNTOS
        # EMPATE SUMA 1 PUNTOS
        # DERROTA SUMA 0 PUNTOS
        listEq1 = dict()
        listEq2 = dict()
        aux1 = []
        aux2 = []
        equipos = []
        cont = 0
        cont2 = 0
        #AGREGAR A DICCIONARIOS LOS EQUIPOS EN LA TEMPORADA
        for x in self.data:
            if x.temporada == fecha:
                if x.equipo1 in listEq1:
                    if listEq1[x.equipo1] == 1:
                        cont  =+ 1
                    listEq1[x.equipo1] += 1
                else:
                    listEq1[x.equipo1] = 1

                if x.equipo2 in listEq2:
                    if listEq2[x.equipo2] == 1:
                        cont2 =+ 1
                    listEq2[x.equipo2] += 1
                else:
                    listEq2[x.equipo2] = 1
        #AGREGAR LAS LLAVES DEL DICCIONARIO A LISTA
        for x in listEq1:
            aux1.append(x)
        for y in listEq2:
            aux2.append(y)   
        #AGREGAR A UNA LISTA LOS EQUIPOS IGUALES EN CADA DICCIONARIO
        for e in aux1:
            for f in aux2:
                if(e==f):
                    equipos.append(e)
                    break

        global texto
        texto = "Archivo de clasificacion de temporada "+str(fecha)+" generado."
        textoTabla = ""
        txtFinal = ('</div>'
            '</body>'
            '</html>')
        
        i = 0
        for x in equipos:
            i += 1
            textoTabla = textoTabla+'<tr>'+'<td>'+str(x)+'</td>'+'<td></td>'+'</tr>'
        
        contenidoHTML = (
            '<!DOCTYPE html>'
            '<html>' 
            '<head> '
            '<meta charset="utf-8"> '
            '<title>REPORTE CLASIFICACION '+str(fecha)+'</title>'
            '<link href="assets/css/bootstrap-responsive.css" type="text/css" rel="stylesheet">'
            '<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css" type="text/css" rel="stylesheet">'
            '<link rel="stylesheet" type="text/css"  href="Style.css">'
            '<link rel="stylesheet" type="text/css" href="bootstrap.css">'
            '</head>'
            '<body>'
            '<div class="container-fluid welcome-page" id="home">'
            '<div class="jumbotron">'
            '<h2>'
            '<span>'+"Clasificacion Temporada "+str(fecha)+'</span>'
            '</h2>'
            '</div>'
            '</div>')
        
        file = open("./REPORTES/"+nombre,"w",encoding = "utf-8")
        file.write(str(contenidoHTML))
        file.write('<h2>'
            '<span>Resumen de clasificacion</span>'
            '</h2>'
            '</br>'
            '</br>')
        
        txtHtml=(
            '<table class="table table-responsive">'
            '<thead>'
            '<tr>'
            '<th scope="col">Equipo</th>'
            '<th scope="col">Puntos</th>'
            '</tr>'
            '</thead>'
            '<tbody>')
        
        for x in equipos:
            i += 1
            txtHtml = txtHtml+'<tr>'+'<td>'+str(x)+'</td>'+'<td></td>'+'</tr>'
        
        file.write(txtHtml)
        file.write('</tbody>'
            '</table>'
            '</div>'
            '</div>')

        file.write(txtFinal)
        file.close()
        webbrowser.open("file:///"+os.getcwd()+"/REPORTES/"+nombre) 
        #print(equipos)
        #print("Cantidad de Equipos en la Temporada: "+str(len(equipos)))
        #print("\n")

        #dicEq = dict(zip(equipos,range(len(equipos))))
        #print(dicEq)

        """aux = []
        valor = 0
        for eq in equipos:
            for x in self.data:
                if x.temporada == fecha:
                    puntos = 0
                    if x.equipo1 == eq:
                        if x.goles1 > x.goles2:
                            puntos += 3
                            if aux is None:
                                aux.append(puntos)
                            else:
                                aux += aux.append(puntos)
                        elif x.goles1 < x.goles2:
                            puntos += 0
                            if aux is None:
                                aux.append(puntos)
                            else:
                                aux += aux.append(puntos)
                        elif x.goles1 == x.goles2:
                            puntos += 1
                            if aux is None:
                                aux.append(puntos)
                            else:
                                aux += aux.append(puntos)
                        print(aux)"""

        #dicEq = dict(zip(equipos,range(len(equipos))))
        
        """#aux = []
        for x in self.puntos:
            for y in dicEq:
                aux = []
                if x.equipo == y:
                    dicEq[y] = self.NoSale(x.puntos)"""
                
        #print(dicEq)


    def opTopSin(self,condicion,fecha,numtop):
        # VICTORIA SUMA 3 PUNTOS
        # EMPATE SUMA 1 PUNTOS
        # DERROTA SUMA 0 PUNTOS
        listEq1 = dict()
        listEq2 = dict()
        aux1 = []
        aux2 = []
        equipos = []
        cont = 0
        cont2 = 0
        #AGREGAR A DICCIONARIOS LOS EQUIPOS EN LA TEMPORADA
        for x in self.data:
            if x.temporada == fecha:
                if x.equipo1 in listEq1:
                    if listEq1[x.equipo1] == 1:
                        cont  =+ 1
                    listEq1[x.equipo1] += 1
                else:
                    listEq1[x.equipo1] = 1

                if x.equipo2 in listEq2:
                    if listEq2[x.equipo2] == 1:
                        cont2 =+ 1
                    listEq2[x.equipo2] += 1
                else:
                    listEq2[x.equipo2] = 1
        #AGREGAR LAS LLAVES DEL DICCIONARIO A LISTA
        for x in listEq1:
            aux1.append(x)
        for y in listEq2:
            aux2.append(y)   
        #AGREGAR A UNA LISTA LOS EQUIPOS IGUALES EN CADA DICCIONARIO
        for e in aux1:
            for f in aux2:
                if(e==f):
                    equipos.append(e)
                    break
                
        global texto
        if condicion == "SUPERIOR":
            for x in range(int(numtop)):
                contenido = "\nTop Superior: "+str(x)+". "
                texto += contenido+equipos[x]
        elif condicion == "INFERIOR":
            for x in range(int(numtop)):
                contenido = "\nTop Inferior "+str(x)+". "
                texto += contenido+equipos[x]
        #print(condicion+"\n"+fecha+"\n"+numtop)
    
    def opTopCon(self,condicion,fecha,numtop):
        # VICTORIA SUMA 3 PUNTOS
        # EMPATE SUMA 1 PUNTOS
        # DERROTA SUMA 0 PUNTOS
        listEq1 = dict()
        listEq2 = dict()
        aux1 = []
        aux2 = []
        equipos = []
        cont = 0
        cont2 = 0
        #AGREGAR A DICCIONARIOS LOS EQUIPOS EN LA TEMPORADA
        for x in self.data:
            if x.temporada == fecha:
                if x.equipo1 in listEq1:
                    if listEq1[x.equipo1] == 1:
                        cont  =+ 1
                    listEq1[x.equipo1] += 1
                else:
                    listEq1[x.equipo1] = 1

                if x.equipo2 in listEq2:
                    if listEq2[x.equipo2] == 1:
                        cont2 =+ 1
                    listEq2[x.equipo2] += 1
                else:
                    listEq2[x.equipo2] = 1
        #AGREGAR LAS LLAVES DEL DICCIONARIO A LISTA
        for x in listEq1:
            aux1.append(x)
        for y in listEq2:
            aux2.append(y)   
        #AGREGAR A UNA LISTA LOS EQUIPOS IGUALES EN CADA DICCIONARIO
        for e in aux1:
            for f in aux2:
                if(e==f):
                    equipos.append(e)
                    break
                
        global texto
        if condicion == "SUPERIOR":
            for x in range(int(numtop)):
                contenido = "\nTop Superior: "+str(x)+". "
                texto += contenido+equipos[x]
        elif condicion == "INFERIOR":
            for x in range(int(numtop)):
                contenido = "\nTop Inferior "+str(x)+". "
                texto += contenido+equipos[x]
        #print(condicion+"\n"+fecha+"\n"+numtop)

    def opPartidos(self,equipo,fecha,nombre,jornadaI,jornadaF):
        global texto
        eq = equipo.replace('"','')
        texto = "\nYa no se me dio para hacer este comando :("+"\n"+str(eq)+" "+str(fecha)
        

    def opAdios(self):
        MessageBox.showinfo(message="Gracias por utilizarme, nos vemos.",title="Bai")
        exit(0)
    
    def EntryBoxAdd(self):
        return texto
    
    def LimpiarText(self):
        global texto
        texto = ""
        return texto