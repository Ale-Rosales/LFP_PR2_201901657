from csv import list_dialects
from dataclasses import dataclass
import imp
from msilib.schema import Error
from typing import TextIO
from matplotlib.cbook import print_cycles

from matplotlib.pyplot import text
from pyparsing import TokenConverter
from Data import Data
import easygui
import re
from tkinter import messagebox as MessageBox
import sys

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
                

    def opJornadaSin(self,jornada,fecha):
        print(jornada+"\n"+fecha)
    
    def opJornadaCon(self,jornada,fecha,nombre):
        print(jornada+"\n"+fecha+"\n"+nombre)


    def opTabla(self):
        pass

    def opPartidos(self):
        pass

    def opTop(self):
        pass


    def opAdios(self):
        MessageBox.showwarning("Alerta", "Gracias por utilizarme, nos vemos.")
        exit(0)

    
    def EntryBoxAdd(self):
        return texto
    
    def LimpiarText(self):
        global texto
        texto = ""
        return texto