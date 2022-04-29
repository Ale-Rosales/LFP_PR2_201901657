class ErrorS:

    def __init__(self, obtenido : str, esperado : str, columna : int) -> None:
        self.esperado = esperado
        self.obtenido = obtenido
        self.columna = columna

    def printError(self):
        print(self.obtenido, self.esperado, self.columna)