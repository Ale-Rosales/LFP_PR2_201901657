import imp
from typing import TextIO

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
                self.crearData(data[0],data[1],data[2],data[3],data[4],data[5],data[6])
                i = i+1
        except Exception as e:
            print(e)

    #PARA VERIFICAR QUE SI ESTA LA DATA CARGADA
    def Print(self):
        for x in self.data:
            print(x.equipo1)

    def opAdios(self):
        MessageBox.showwarning("Alerta", "Gracias por utilizarme, nos vemos.")
        exit(0)
    
    def opResultado(self,equipo1,equipo2,fecha):
        global texto
        cadena1 = equipo1.replace('"','')
        cadena2 = equipo2.replace('"','')
        #print(cadena1+"\n"+cadena2+"\n"+fecha)
        #print("\n")
        try:
            for x in self.data:
                if x.temporada == fecha and x.equipo1 == cadena1 and x.equipo2 == cadena2:
                    texto = "El resultado de este partido fue: "+x.equipo1+": "+x.goles1+" - "+x.equipo2+": "+x.goles2
        except:
            MessageBox.showwarning("Alerta", "Parece que ocurrio un error.")

    def EntryBoxAdd(self):
        return texto
    
    def LimpiarText(self):
        global texto
        texto = ""
        return texto