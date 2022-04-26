from tkinter import *
from tkinter import messagebox as MessageBox
import os
import webbrowser
from Lexico import Lexico

lexico = Lexico()

class Interfaz:
    def __init__(self):
        raiz = Tk()
        raiz.title("La Liga Bot")
        raiz.resizable(0,0)
        raiz.iconbitmap("Icono.ico")
        miFrame = Frame()
        miFrame.pack()
        miFrame.config(width="750",height="650")
        #AREA DEL BOT
        self.area = Text(miFrame)
        self.area.place(x=10,y=10)
        #self.area.insert(1.0, "Bienvenido a La Liga Bot")
        self.area.config(width=68,height=36)
        self.area.insert(-1.,"Bienvenido a La Liga Bot")
        #BOTONES
        bErrores = Button(miFrame, text="Reporte Errores",font=("Comic Sans MS", 10), width=15, height=1)
        bErrores.place(x=590, y=15)
        bClearE = Button(miFrame, text="Limpiar Log Errores",font=("Comic Sans MS", 10), width=15, height=1)
        bClearE.place(x=590, y=60)
        bTokens = Button(miFrame, text="Reporte Tokens",font=("Comic Sans MS", 10), width=15, height=1)
        bTokens.place(x=590, y=105)
        bClearT = Button(miFrame, text="Limpiar Log Tokens",font=("Comic Sans MS", 10), width=15, height=1)
        bClearT.place(x=590, y=150)
        bUsuario = Button(miFrame, text="Manual Usuario",font=("Comic Sans MS", 10), width=15, height=1)
        bUsuario.place(x=590, y=195)
        bTecnico = Button(miFrame, text="Manual Tecnico",font=("Comic Sans MS", 10), width=15, height=1)
        bTecnico.place(x=590, y=240)
        bEnviar = Button(miFrame, text="Enviar",font=("Comic Sans MS", 10), width=15, height=1,command=self.EntryBox)
        bEnviar.place(x=590, y=601)
        #AREA COMNADOS
        self.texto = StringVar()
        self.comandos = Entry(miFrame, textvariable=self.texto)
        self.comandos.insert(0,"Escribe tu comando aqui")
        self.comandos.config(state=DISABLED)
        self.comandos.place(x=10, y= 605, width=550, height=25)
        def on_click(event):
            self.comandos.config(state=NORMAL)
            self.comandos.delete(0,END)
            self.comandos.unbind('<Button-1>', on_click_id)
        
        on_click_id = self.comandos.bind('<Button-1>', on_click)

        raiz.mainloop()
    
    #-------------------------------------FUNCIONALIDAD INTERFAZ-------------------------------------
    def EntryBox(self):
        texto = self.texto.get()
        lexico.Analizar(texto)
        lexico.printTokens()
        comando = self.texto.get()
        agregar = comando+'\n'+'\n'
        self.area.insert(1.0,agregar)
        self.comandos.delete(0,END)

    def SaveTokens(self):
        lexico.printTokens()
    
    
    #-----------BOTONES DOCUMENTACION-----------
    def Usuario(self):
        webbrowser.open("file:///"+os.getcwd()+"/DOCUMENTACION/ManualUsuario.pdf")

    def Tecnico(self):
        webbrowser.open("file:///"+os.getcwd()+"/DOCUMENTACION/ManualTecnico.pdf")
