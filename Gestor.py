from itertools import starmap
from pyparsing import TokenConverter
from Data import Data
import easygui
import re
from tkinter import messagebox as MessageBox
import sys
import random
import os
import webbrowser

texto = ""

class Gestor:

    def __init__(self):
        self.data = []

    def crearData(self,fecha,temporada,jornada,equipo1,equipo2,goles1,goles2):
        self.data.append(Data(fecha,temporada,jornada,equipo1,equipo2,goles1,goles2))
    
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
        #EMPATE SUMA 1 PUNTOS
        #DERROTA SUMA 0 PUNTOS
        global texto
        epPu = 0
        #eq = ""
        for x in self.data:
            if x.temporada == fecha:
                """if x.goles1 > x.goles2:
                    epPu += 3
                elif x.goles1 < x.goles2:
                    epPu += 1
                elif x.goles1 == x.goles2:
                    epPu += 0"""
        #print(x.equipo1+" "+str(epPu))
        #print(fecha+"\n"+nombre)
    
    def opTablaCon(self,fecha,nombre):
        print(fecha+"\n"+nombre)

    def opTopSin(self,condicion,fecha,numtop):
        global texto
        if condicion == "SUPERIOR":
            for x in self.data:
                if x.temporada == fecha:
                    pass
        elif condicion == "INFERIOR":
            for x in self.data:
                if x.temporada == fecha:
                    pass
        #print(condicion+"\n"+fecha+"\n"+numtop)
    
    def opTopCon(self,condicion,fecha,numtop):
        global texto
        if condicion == "SUPERIOR":
            for x in self.data:
                if x.temporada == fecha:
                    pass
        elif condicion == "INFERIOR":
            for x in self.data:
                if x.temporada == fecha:
                    pass
        #print(condicion+"\n"+fecha+"\n"+numtop)

    def opPartidos(self):
        pass

    def opAdios(self):
        MessageBox.showinfo(message="Gracias por utilizarme, nos vemos.",title="Bai")
        exit(0)

    
    def EntryBoxAdd(self):
        return texto
    
    def LimpiarText(self):
        global texto
        texto = ""
        return texto