import imp
from Data import Data
import easygui
import re

class Gestor:

    def __init__(self) -> None:
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

    def Print(self):
        for x in self.data:
            print(x.equipo1)