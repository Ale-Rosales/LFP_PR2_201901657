from Interfaz import Interfaz
from Gestor import Gestor

gestor = Gestor()

if __name__ == '__main__':
    #gestor.Print()
    gestor.cargarData()
    app = Interfaz(gestor)
    #Gestor.cargarData()
