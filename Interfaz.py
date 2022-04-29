from tkinter import *
from tkinter import messagebox as MessageBox
import os
import webbrowser
from Lexico import Lexico
from Sintactico import Sintactico
import time

lexico = Lexico()
erroresS = []

class Interfaz:
    def __init__(self,gestor):
        self.gestor = gestor
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
        self.area.config(width=70,height=36)
        self.area.insert(-1.,"Bot: Bienvenido a La Liga Bot\n")
        self.area.configure(foreground="red")
        #BOTONES
        bErrores = Button(miFrame, text="Reporte Errores",font=("Comic Sans MS", 10), width=15, height=1, command=self.ErroresR)
        bErrores.place(x=590, y=15)
        bClearE = Button(miFrame, text="Limpiar Log Errores",font=("Comic Sans MS", 10), width=15, height=1, command=self.clearLogError)
        bClearE.place(x=590, y=60)
        bTokens = Button(miFrame, text="Reporte Tokens",font=("Comic Sans MS", 10), width=15, height=1, command=self.ReporteTokens)
        bTokens.place(x=590, y=105)
        bClearT = Button(miFrame, text="Limpiar Log Tokens",font=("Comic Sans MS", 10), width=15, height=1, command=self.clearLogToken)
        bClearT.place(x=590, y=150)
        bUsuario = Button(miFrame, text="Manual Usuario",font=("Comic Sans MS", 10), width=15, height=1, command=self.Usuario)
        bUsuario.place(x=590, y=195)
        bTecnico = Button(miFrame, text="Manual Tecnico",font=("Comic Sans MS", 10), width=15, height=1, command=self.Tecnico)
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

    #---------------BOTON ENVIAR---------------
    def EntryBox(self):
        #ESTO SE ENVIA AL ANALIZADOR
        texto = self.texto.get()
        lexico.Analizar(texto)
        lexico.AnalizarR(texto)
        lexico.printTokens()
        #lexico.printErrores()
        listToke = lexico.listaTokens
        sintactico = Sintactico(listToke, self.gestor)
        sintactico.AnalizarS()
        global erroresS
        erroresS = sintactico.errores
        #sintactico.printErrorS()
    
        #ESTO SE ENVIA AL AREABOX DEL BOT
        if texto == "":
            pass
        else:
            agregar = '\n'+"Yo: "+texto+'\n'
            #agregar = texto+'\n'+'\n'
            self.area.insert(END,agregar)
            self.area.configure(foreground="green")
            self.comandos.delete(0,END)

        #REGRESA LA RESPUESTA DEL ANALIZADOR SINTACTICO
        add = self.gestor.EntryBoxAdd()
        if add == "":
            pass
        else:
            addT = '\n'+"Bot: "+add+'\n'
            #addT = add+'\n'+'\n'
            self.area.insert(END,addT)
            self.area.configure(foreground="blue")
        add = self.gestor.LimpiarText()
        addT = ""
        #print(agregar)

    
    #---------------BOTONES LogToken/LogError---------------

    def SaveTokens(self):
        #lexico.printTokens()
        lexico.printTokensR()
    
    def SaveErrores(self):
        lexico.printErroresR()
        #sintactico.ErroresS()
    
    def clearLogToken(self):
        lexico.clearTokensR()
        MessageBox.showinfo(message="Log de tokens eliminado", title="Tokens")
    
    def clearLogError(self):
        global erroresS
        erroresS.clear()
        lexico.clearErroresR()
        MessageBox.showinfo(message="Log de errores eliminado", title="Errores")
        #sintactico.clearErroresS()

    
    #---------------BOTONES ReporteTokens/ReporteErrores---------------
    def ReporteTokens(self):
        tokens = lexico.tokensR
        if len(tokens) == 0:
            MessageBox.showwarning("Alerta", "Sin tokens para generar reporte")
        else:
            textoTabla = ""
            txtFinal = ('</div>'
            '</body>'
            '</html>')

            i = 0
            for x in tokens:
                i += 1
                textoTabla = textoTabla+'<tr>'+'<td>'+str(x.lexema)+'</td>'+'<td>'+str(x.linea)+'</td>'+'<td>'+str(x.columna)+'</td>'+'<td>'+str(x.tipo)+'</td>'+'</tr>'
            
            contenidoHTML = (
            '<!DOCTYPE html>'
            '<html>' 
            '<head> '
            '<meta charset="utf-8"> '
            '<title>Reporte Tokens</title>'
            '<link href="assets/css/bootstrap-responsive.css" type="text/css" rel="stylesheet">'
            '<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css" type="text/css" rel="stylesheet">'
            '<link rel="stylesheet" type="text/css"  href="Style.css">'
            '<link rel="stylesheet" type="text/css" href="bootstrap.css">'
            '</head>'
            '<body>'
            '<div class="container-fluid welcome-page" id="home">'
            '<div class="jumbotron">'
            '<h1>'
            '<span>Reporte Tokens</span>'
            '</h1>'
            '</div>'
            '</div>')

            file = open("./REPORTES/ReporteTokens.html","w")
            file.write(str(contenidoHTML))
            file.write('<h2>'
            '<span>Analisis Realizado</span>'
            '</h2>')

            txtHtml=(
            '<table class="table table-responsive">'
            '<thead>'
            '<tr>'
            '<th scope="col">Lexema</th>'
            '<th scope="col">Linea</th>'
            '<th scope="col">Columna</th>'
            '<th scope="col">Tipo</th>'
            '</tr>'
            '</thead>'
            '<tbody>')

            for x in tokens:
                i += 1
                txtHtml = txtHtml+'<tr>'+'<td>'+str(x.lexema)+'</td>'+'<td>'+str(x.linea)+'</td>'+'<td>'+str(x.columna)+'</td>'+'<td>'+str(x.tipo)+'</td>'+'</tr>'

            file.write(txtHtml)
            file.write('</tbody>'
            '</table>'
            '</div>'
            '</div>')

            file.write(txtFinal)
            file.close()
            webbrowser.open("file:///"+os.getcwd()+"/REPORTES/ReporteTokens.html")
    
    def ReporteErrores(self):
        global erroresS
        errores = lexico.erroresR
        if len(errores) == 0:
            MessageBox.showwarning("Alerta", "Sin errores para generar reporte")
        else:
            textoTabla = ""
            txtFinal = ('</div>'
            '</body>'
            '</html>')

            i = 0
            for x in errores:
                i += 1
                textoTabla = textoTabla+'<tr>'+'<td>'+str(x.descripcion)+'</td>'+'<td>'+str(x.linea)+'</td>'+'<td>'+str(x.columna)+'</td>'+'</tr>'

            textoTabla2 = ""

            t = 0
            for y in erroresS:
                i += 1
                textoTabla2 = textoTabla2+'<tr>'+'<td>'+str(y.obtenido)+'</td>'+'<td>'+str(y.esperado)+'</td>'+'<td>'+str(y.columna)+'</td>'+'</tr>'

            contenidoHTML = (
            '<!DOCTYPE html>'
            '<html>' 
            '<head> '
            '<meta charset="utf-8"> '
            '<title>Reporte Tokens</title>'
            '<link href="assets/css/bootstrap-responsive.css" type="text/css" rel="stylesheet">'
            '<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css" type="text/css" rel="stylesheet">'
            '<link rel="stylesheet" type="text/css"  href="Style.css">'
            '<link rel="stylesheet" type="text/css" href="bootstrap.css">'
            '</head>'
            '<body>'
            '<div class="container-fluid welcome-page" id="home">'
            '<div class="jumbotron">'
            '<h1>'
            '<span>Reporte Errores</span>'
            '</h1>'
            '</div>'
            '</div>')
            
            file = open("./REPORTES/ReporteErrores.html","w")
            file.write(str(contenidoHTML))
            file.write('<h2>'
            '<span>Analisis Lexico Realizado</span>'
            '</h2>')

            txtHtml=(
            '<table class="table table-responsive">'
            '<thead>'
            '<tr>'
            '<th scope="col">Descripcion</th>'
            '<th scope="col">Linea</th>'
            '<th scope="col">Columna</th>'
            '</tr>'
            '</thead>'
            '<tbody>')

            for x in errores:
                i += 1
                txtHtml = txtHtml+'<tr>'+'<td>'+str(x.descripcion)+'</td>'+'<td>'+str(x.linea)+'</td>'+'<td>'+str(x.columna)+'</td>'+'</tr>'

            file.write(txtHtml)
            
            file.write('</br>'
            '</br>'
            '</br>'
            '<h2>'
            '<span>Analisis Sintactico Realizado</span>'
            '</h2>')

            txtHtml2=(
            '<table class="table table-responsive">'
            '<thead>'
            '<tr>'
            '<th scope="col">Obtenido</th>'
            '<th scope="col">Esperado</th>'
            '<th scope="col">Columna</th>'
            '</tr>'
            '</thead>'
            '<tbody>')

            for y in erroresS:
                i += 1
                textoTabla2 = textoTabla2+'<tr>'+'<td>'+str(y.obtenido)+'</td>'+'<td>'+str(y.esperado)+'</td>'+'<td>'+str(y.columna)+'</td>'+'</tr>'

            
            file.write(txtHtml2)
            file.write('</tbody>'
            '</table>'
            '</div>'
            '</div>')

            file.write(txtFinal)
            file.close()
            webbrowser.open("file:///"+os.getcwd()+"/REPORTES/ReporteErrores.html")
        
    def ErroresR(self):
        global erroresS
        errores = lexico.erroresR
        textoTabla = ""
        txtFinal = ('</div>'
        '</body>'
        '</html>')

        i = 0
        for x in errores:
            i += 1
            textoTabla = textoTabla+'<tr>'+'<td>'+str(x.descripcion)+'</td>'+'<td>'+str(x.linea)+'</td>'+'<td>'+str(x.columna)+'</td>'+'</tr>'

        textoTabla2 = ""

        t = 0
        for y in erroresS:
            t += 1
            textoTabla2 = textoTabla2+'<tr>'+'<td>'+str(y.obtenido)+'</td>'+'<td>'+str(y.esperado)+'</td>'+'<td>'+str(y.columna)+'</td>'+'</tr>'

        contenidoHTML = (
            '<!DOCTYPE html>'
            '<html>' 
            '<head> '
            '<meta charset="utf-8"> '
            '<title>Reporte Tokens</title>'
            '<link href="assets/css/bootstrap-responsive.css" type="text/css" rel="stylesheet">'
            '<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css" type="text/css" rel="stylesheet">'
            '<link rel="stylesheet" type="text/css"  href="Style.css">'
            '<link rel="stylesheet" type="text/css" href="bootstrap.css">'
            '</head>'
            '<body>'
            '<div class="container-fluid welcome-page" id="home">'
            '<div class="jumbotron">'
            '<h1>'
            '<span>Reporte Errores</span>'
            '</h1>'
            '</div>'
            '</div>')
            
        file = open("./REPORTES/ReporteErrores.html","w")
        file.write(str(contenidoHTML))
        file.write('<h2>'
            '<span>Analisis Realizado</span>'
            '</h2>')

        txtHtml=(
            '<table class="table table-responsive">'
            '<thead>'
            '<tr>'
            '<th scope="col">Descripcion</th>'
            '<th scope="col">Linea</th>'
            '<th scope="col">Columna</th>'
            '</tr>'
            '</thead>'
            '<tbody>')

        for x in errores:
            i += 1
            txtHtml = txtHtml+'<tr>'+'<td>'+str(x.descripcion)+'</td>'+'<td>'+str(x.linea)+'</td>'+'<td>'+str(x.columna)+'</td>'+'</tr>'

        file.write(txtHtml)

        txtHtml2=(
            '<table class="table table-responsive">'
            '<thead>'
            '<tr>'
            '<th scope="col">Obtenido</th>'
            '<th scope="col">Esperado</th>'
            '<th scope="col">Columna</th>'
            '</tr>'
            '</thead>'
            '<tbody>')

        for y in erroresS:
            t += 1
            txtHtml2 = txtHtml2+'<tr>'+'<td>'+str(y.obtenido)+'</td>'+'<td>'+str(y.esperado)+'</td>'+'<td>'+str(y.columna)+'</td>'+'</tr>'

            
        file.write(txtHtml2)
        file.write('</tbody>'
            '</table>'
            '</div>'
            '</div>')

        file.write(txtFinal)
        file.close()
        webbrowser.open("file:///"+os.getcwd()+"/REPORTES/ReporteErrores.html")

        
    

    #---------------BOTONES DOCUMENTACION---------------
    def Usuario(self):
        webbrowser.open("file:///"+os.getcwd()+"/DOCUMENTACION/ManualUsuario.pdf")

    def Tecnico(self):
        webbrowser.open("file:///"+os.getcwd()+"/DOCUMENTACION/ManualTecnico.pdf")
