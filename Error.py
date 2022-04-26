from msilib.schema import CompLocator
from pyparsing import line


class Error:

    def __init__(self, descripcion : str, linea : int, columna : int) -> None:
        self.descripcion = descripcion
        self.linea = linea
        self.columna = columna

    def printError(self):
        print(self.descripcion, self.linea, self.columna)