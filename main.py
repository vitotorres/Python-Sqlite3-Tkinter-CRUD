from tkinter import ttk
from tkinter import *
from tkinter import messagebox

import pandas as pd

import sqlite3


class Product:

    def __init__(self, window):
        self.wind = window
        self.wind.title('Products Aplication')

        # Menu Bar ----------------------------------------------------------------------------------------------------------------------------

        barraMenu=Menu(window)
        window.config(menu=barraMenu, width=300, height=300)
        bbddMenu=Menu(barraMenu, tearoff=0)
        bbddMenu.add_command(label="Conectar", command=self.crearBBDD)
        bbddMenu.add_command(label="Mostrar BBDD")
        bbddMenu.add_command(label="Salir", command=self.salirAplicacion)

        borrarMenu=Menu(barraMenu, tearoff=0)
        borrarMenu.add_command(label="Borrar campos", command=self.limpiarCampos)

        crudMenu=Menu(barraMenu, tearoff=0)
        crudMenu.add_command(label="Insertar", command=self.insertar)
        crudMenu.add_command(label="Leer", command=self.leer)
        crudMenu.add_command(label="Actualizar", command=self.actualizar)
        crudMenu.add_command(label="Borrar", command=self.eliminar)

        barraMenu.add_cascade(label="BBDD", menu=bbddMenu)
        barraMenu.add_cascade(label="Borrar", menu=borrarMenu)
        barraMenu.add_cascade(label="CRUD", menu=crudMenu)

        # Entry box ------------------------------------------------------------------------------------------------------------

        miFrame=Frame(window)
        miFrame.config( bg="#3A405A")
        miFrame.pack()

        self.miId=StringVar()
        self.miNombre=StringVar()
        self.miPrecio=StringVar()

        cuadroID=Entry(miFrame, bg="#F9DEC9", textvariable=self.miId)
        cuadroID.grid(row=0, column=1, padx=10, pady=10)

        cuadroNombre=Entry(miFrame, bg="#F9DEC9", textvariable=self.miNombre)
        cuadroNombre.grid(row=1, column=1, padx=10, pady=10)
        #cuadroNombre.config(fg="red", justify="right")


        cuadroPrecio=Entry(miFrame, bg="#F9DEC9", textvariable=self.miPrecio)
        cuadroPrecio.grid(row=2, column=1, padx=10, pady=10)

        # Labels -----------------------------------------------------------------------------------------------------------------------------------------

        idLabel=Label(miFrame, text="Id:", bg= "#3A405A", fg="#F9DEC9")
        idLabel.grid(row=0, column=0, sticky="e", padx=10, pady=10)


        nombreLabel=Label(miFrame, text="Nombre:", bg= "#3A405A", fg="#F9DEC9")
        nombreLabel.grid(row=1, column=0, sticky="e", padx=10, pady=10)

        precioLabel=Label(miFrame, text="Precio:", bg= "#3A405A", fg="#F9DEC9")
        precioLabel.grid(row=2, column=0, sticky="e", padx=10, pady=10)

        # Buttons ------------------------------------------------------------------------------------------------------------------------------------------

        miFrame2=Frame(window)
        miFrame2.config( bg="#3A405A")
        miFrame2.pack()

        botonCrear=Button(miFrame2, text="Insertar", bg="#AEC5EB", command= self.insertar)
        botonCrear.grid(row=1, column=0, sticky="e", padx=10, pady=10)

        botonLeer=Button(miFrame2, text="Leer", bg="#AEC5EB", command=self.leer)
        botonLeer.grid(row=1, column=1, sticky="e", padx=10, pady=10)

        botonActualizar=Button(miFrame2, text="Actualizar", bg="#AEC5EB", command=self.actualizar)
        botonActualizar.grid(row=1, column=2, sticky="e", padx=10, pady=10)

        botonBorrar=Button(miFrame2, text="Borrar", bg="#AEC5EB", command=self.eliminar)
        botonBorrar.grid(row=1, column=3, sticky="e", padx=10, pady=10)

        # BBDD -----------------------------------------------------------------------

        self.miConexion=sqlite3.connect("articulos.db")

        self.miCursor=self.miConexion.cursor()

        # Draw table -----------------------------------------------------------------------------
        self.miFrame3=Frame(window)
        self.miFrame3.pack()

        self.tabla()

    def crearBBDD(self):

        try:

            self.miCursor.execute('''
                CREATE TABLE DATOSARTICULOS(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NOMBRE VARCHAR(50),
                PRECIO FLOAT(64)
                )''')

            messagebox.showinfo("BBDD", "BBDD creada con éxito")

        except:

            messagebox.showwarning("¡Atención!", "La BBDD ya existe")

    def salirAplicacion(self):
        valor=messagebox.askquestion("Salir", "¿Deseas salir de la aplicacion?")

        if valor=="yes":
            window.destroy()

    def insertar(self):

        varGestion=(self.miId.get(),self.miNombre.get(), self.miPrecio.get())

        self.miCursor.execute("INSERT INTO DATOSARTICULOS VALUES(?,?,?)", varGestion)

        self.miConexion.commit()

        messagebox.showinfo("BBDD", "Registro insertado con exito")

        self.tabla()

    def limpiarCampos(self):
        self.miId.set("")
        self.miNombre.set("")
        self.miPrecio.set("")

    def leer(self):
        varSelection=(self.miId.get())
        self.miCursor.execute("SELECT * FROM DATOSARTICULOS WHERE Id =" + varSelection )

        elArticulo=self.miCursor.fetchall()

        for usuario in elArticulo:
            self.miId.set(usuario[0])
            self.miNombre.set(usuario[1])
            self.miPrecio.set(usuario[2])

        self.miConexion.commit()

    def actualizar(self):

        self.miCursor.execute("UPDATE DATOSARTICULOS SET NOMBRE='" + self.miNombre.get() +
            "', PRECIO='" + self.miPrecio.get() + 
            "' WHERE ID=" + self.miId.get())
        
        self.miConexion.commit()

        messagebox.showinfo("BBDD", "Registro actualizado con éxito")

        self.tabla()

    def eliminar(self):
        
        self.miCursor.execute("DELETE FROM DATOSARTICULOS WHERE ID=" + self.miId.get())

        self.miConexion.commit()

        messagebox.showinfo("BBDD", "Registro borrado con éxito")

        self.tabla()

    def tabla(self):
         
        self.miCursor.execute("SELECT * FROM DATOSARTICULOS ORDER BY Id DESC")

        listaUsuarios=self.miCursor.fetchall()

        listaArticulos= pd.DataFrame( data= listaUsuarios, columns= ("Id", "Articulo", "Precio"))

        scroll=Scrollbar(self.miFrame3)
        scroll.grid(row=0, column=1, sticky="nsew")

        tabla=ttk.Treeview(self.miFrame3 , columns = ('#0', '#1','#2', '#3'), yscrollcommand=scroll.set)
        tabla.grid(row= 0, column= 0)
        tabla.heading('#1', text = 'Id', anchor = CENTER)
        tabla.heading('#2', text = 'Articulo', anchor = CENTER)  
        tabla.heading('#3', text = 'Precio', anchor = CENTER) 
        tabla.column("#0", width=0, anchor=CENTER)
        tabla.column("#1", width=80, anchor=CENTER)
        tabla.column("#2", width=80, anchor=CENTER)
        tabla.column("#3", width=80, anchor=CENTER)

        numeroFilas=(len(listaArticulos.index))
        i = 0

        while i < numeroFilas :
            tabla.insert("",0,  values=(listaArticulos. iloc[i,0],listaArticulos.iloc[i,1],listaArticulos.iloc[i,2]))
            i = i + 1   

        scroll.config(orient=VERTICAL, command=tabla.yview, width=30)


if __name__ == '__main__':
    window = Tk()
    window.geometry("800x600")
    window.config(bg="#3A405A")
    aplication = Product(window)
    window.mainloop()

      