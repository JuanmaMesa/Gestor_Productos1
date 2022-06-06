from tkinter import ttk
from tkinter import *
from tkinter import messagebox as MessageBox

import sqlite3



class Producto:
    db = "database/productos.db"







    def __init__(self,root):
        self.ventana = root
        self.ventana.title("App Gestor de Productos")
        #self.ventana.config(width='8', height='10')
        #self.ventana.resizable(1,1)
        self.ventana['bg']='#C0C0C0'

        # Creacion del contenedor Frame principal
        frame = LabelFrame(self.ventana, text="Registrar un nuevo Producto", font=("Candara", 16, "bold"), background="#C0C0C0")
        frame.grid(row=0, column=0, columnspan=5,pady=20, sticky=E + W )

        # Label Nombre
        self.etiqueta_nombre = Label(frame, text="Nombre: ",background='#C0C0C0', font=("Calibri", 10, "bold"))
        # Etiqueta de texto ubicada
        self.etiqueta_nombre.grid(row=0, column=1,)  # Posicionamiento a traves de grid
        # Entry Nombre (caja de texto que recibira el nombre)
        self.nombre = Entry(frame)  # Caja de texto (input de texto) ubicada en el frame
        self.nombre.focus()  # Para que el foco del raton vaya a este Entry al inicio
        self.nombre.grid(row=0, column=2)

        # Label precio
        self.etiqueta_precio = Label(frame, text="Precio: ", background='#C0C0C0', font=("Calibri", 10, "bold"))
        self.etiqueta_precio.grid(row=1, column=1)
        #Entry Precio (caja de texto que recibira el precio)
        self.precio = Entry(frame)
        self.precio.grid(row=1, column=2)

        # Label Unidades
        self.etiqueta_unidades = Label(frame, text="Unidades: ", background='#C0C0C0', font=("Calibri", 10, "bold"))
        self.etiqueta_unidades.grid(row=2, column=1)
        # Entry unidades
        self.unidades = Entry(frame)
        self.unidades.grid(row=2, column=2)

        # Boton guardar
        s = ttk.Style()
        s.configure("my.TButton", font=("Calibri", 12, "bold"), background='#F5F5F5')
        self.boton_aniadir = ttk.Button(frame, text= "Guardar Producto", command= self.add_producto, style='my.TButton')
        self.boton_aniadir.grid(row=3,column=0, columnspan=4, sticky= E+W)


        # Mensaje informativo para el usuario
        self.mensaje = Label(text="", fg="red", font=("Calibri", 12))
        self.mensaje.grid(row=3,column=0, columnspan=2, sticky=E+W)





        # TABLA DE PRODUCTOS
        #Estilo de la tabla
        style = ttk.Style()
        # Modificación fuente de la tabla
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=("Calibri", 11))
        # Modificación fuente de las cabeceras
        style.configure("mystyle.Treeview.Heading", font=("Calibri", 13,"bold"),background='#8CBED6')
        # Estructura de la tabla
        encabezado = ["Precio", "Unidades"] # Lista para el encabezado de la Tabla
        self.tabla = ttk.Treeview(height=20, columns=(encabezado), style="mystyle.Treeview")
        self.tabla.grid(row=4, column=0, columnspan=4)
        self.tabla.heading('#0', text='Nombre', anchor=CENTER)  # Encabezado 0

        for i in encabezado:
            self.tabla.heading(column=f'{i}', text=f'{i}', anchor=CENTER)
        self.get_productos()

        # Botones de Eliminar y Editar
        s = ttk.Style()
        s.configure("my.TButton",font=("Calibri", 10, "bold"))
        s.configure("eliminar.TButton",background="#FFC0CB", font=("Calibri", 10, "bold")) #Boton personalizado de eliminar
        self.boton_eliminar = ttk.Button(text= "ELIMINAR", command = self.mensaje_prueba,style="eliminar.TButton")
        s.map("eliminar.TButton", foreground=[("active","#FFA500")])
        self.boton_eliminar.grid(row=5,column=0,columnspan=2, sticky= W + E)
        self.boton_editar = ttk.Button(text= "EDITAR", command= self.edit_producto, style="my.TButton")
        self.boton_editar.grid(row=5, column=2, columnspan=2, sticky= W + E)
        s.configure("my.TButton", font=("Calibri", 10, "bold"))

        # prueba de botones
        #self.boton_ventana = ttk.Button(text="clicma", command=self.test)

        #self.boton_ventana.grid(row=5, column=3)


    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
        return resultado

    def get_productos(self):
        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)
        query = "SELECT * FROM producto ORDER BY Nombre DESC"
        registros = self.db_consulta(query)


        for fila in registros:
            print(fila)
            self.tabla.insert("", 0, text=fila[1], values=(fila[2], fila[3]))

    def validacion_nombre(self):
        nombre_introducido_por_usuario = self.nombre.get()
        return len(nombre_introducido_por_usuario) != 0

    def validacion_precio(self):
        precio_introducido_por_usuario = self.precio.get()
        return len(precio_introducido_por_usuario) != 0
    def validacion_unidades(self):
        unidades_introducido_por_usuario= self.unidades.get()
        return len(unidades_introducido_por_usuario) != 0

    def add_producto(self):
        if self.validacion_nombre() and self.validacion_precio() and self.validacion_unidades():
            query = "INSERT INTO producto VALUES(NULL, ?, ?, ?)"
            parametros=(self.nombre.get(), self.precio.get(), self.unidades.get())
            self.db_consulta(query, parametros)
            self.mensaje["text"] = "Producto '{}' se ha añadido con éxito".format(self.nombre.get())
            self.mensaje["fg"] ="green"
            self.nombre.delete(0, END)
            self.precio.delete(0, END)
            self.unidades.delete(0, END)


        elif self.validacion_nombre() and self.validacion_precio()==False  and self.validacion_unidades():
            print("El precio es obligatorio")
            self.mensaje["text"] = "El precio es obligatorio"
        elif self.validacion_nombre() == False and self.validacion_precio() and self.validacion_unidades():
            print("El nombre es obligatorio")
            self.mensaje["text"] = "El nombre es obligatorio"
        elif self.validacion_nombre()  and self.validacion_precio() and self.validacion_unidades()== False:
            self.mensaje["text"] = "Las unidades son obligatorias"
        else:
            print("Todas las casillas son obligatorias")
            self.mensaje["text"] = "Todas las casillas son obligatorias"

        self.get_productos()

    def del_producto(self):
       # Comprobacion de que se seleccione un producto para poder eliminarlo
        self.mensaje["text"] = ""
        try:
            self.tabla.item(self.tabla.selection())["text"][0]
        except IndexError as e:
            self.mensaje["text"] = "Por favor, seleccione un producto"


        nombre = self.tabla.item(self.tabla.selection())["text"]
        query = "DELETE FROM producto WHERE nombre = ?"
        self.db_consulta(query, (nombre,))
        self.mensaje["text"] = "El producto {} ha sido eliminado con éxito".format(nombre)
        #self.ventana_mensaje_eliminar.destroy()
        self.get_productos() # Actualizar la tabla productos

    def edit_producto(self):

            # Comprobacion de que se seleccione un producto para poder editarlo
            self.mensaje["text"] = ""
            try:
                self.tabla.item(self.tabla.selection())["text"][0]
            except IndexError as e:
                self.mensaje["text"] = "Por favor, seleccione un producto"
                return

            nombre = self.tabla.item(self.tabla.selection())["text"]
            old_precio = self.tabla.item(self.tabla.selection())["values"][0]

            # ventana nueva (Editar producto)
            self.ventana_editar = Toplevel()  # creacion de una ventana
            self.ventana_editar.title = "Editar Producto"
            self.ventana_editar.resizable(1, 1)

            titulo = Label(self.ventana_editar, text="Edición de Productos", font=("Calibri", 16, "bold"))
            titulo.grid(column=0, row=0)

            # Creación del contenedor frame de la ventana de Editar producto
            frame_ed = LabelFrame(self.ventana_editar, text="Editar el siguiente Producto",
                                  font=("Candara", 12, "bold"))
            frame_ed.grid(row=1, column=0, columnspan=20, pady=20)

            # Label nombre antiguo
            self.etiqueta_nombre_antiguo = Label(frame_ed, text=" Nombre antiguo: ", font=('Calibri', 13))
            self.etiqueta_nombre_antiguo.grid(row=2, column=0)
            # Entry nombre antiguo (texto que no se podra modificar)
            self.input_nombre_antiguo = Entry(frame_ed, textvariable=StringVar(self.ventana_editar, value=nombre),
                                              state="readonly", font=('Calibri', 13))
            self.input_nombre_antiguo.grid(row=2, column=1)

            # Label Nombre nuevo
            self.etiqueta_nombre_nuevo = Label(frame_ed, text=" Nombre nuevo: ", font=('Calibri', 13))
            self.etiqueta_nombre_nuevo.grid(row=3, column=0)
            # Entry Nombre nuevo
            self.input_nombre_nuevo = Entry(frame_ed, font=('Calibri', 13))
            self.input_nombre_nuevo.grid(row=3, column=1)
            self.input_nombre_nuevo.focus()

            # Label Precio antiguo
            self.etiqueta_precio_antiguo = Label(frame_ed, text=" Precio antiguo: ", font=('Calibri', 13))
            self.etiqueta_precio_antiguo.grid(row=4, column=0)
            # Entry Precio antiguo
            self.input_precio_antiguo = Entry(frame_ed, textvariable=StringVar(self.ventana_editar, value=old_precio),
                                              state="readonly", font=('Calibri', 13))
            self.input_precio_antiguo.grid(row=4, column=1)

            # Label precio nuevo
            self.etiqueta_precio_nuevo = Label(frame_ed, text=" Precio nuevo: ", font=('Calibri', 13))
            self.etiqueta_precio_nuevo.grid(row=5, column=0)
            # Entry precio nuevo
            self.input_precio_nuevo = Entry(frame_ed, font=('Calibri', 13))
            self.input_precio_nuevo.grid(row=5, column=1)

            # Boton de actualizar producto
            self.boton_actualizar = ttk.Button(frame_ed, text="Actualizar Producto", style="my.TButton",
                                               command=lambda:

                                                self.actualizar_productos(self.input_nombre_nuevo.get(),
                                                                         self.input_nombre_antiguo.get(),
                                                                         self.input_precio_nuevo.get(),
                                                                         self.input_precio_antiguo.get()))

            self.boton_actualizar.grid(row=6, columnspan=2, sticky=W + E)

    def actualizar_productos(self,nuevo_nombre, antiguo_nombre, nuevo_precio, antiguo_precio):
        producto_modificado = False
        query = "UPDATE producto SET nombre = ?, precio = ? WHERE nombre =? AND precio =?"
        if nuevo_nombre != '' and nuevo_precio != '':
            parametros = (nuevo_nombre, nuevo_precio, antiguo_nombre, antiguo_precio)
            producto_modificado = True
        elif nuevo_nombre != '' and nuevo_precio == '':
            parametros = (nuevo_nombre, antiguo_precio, antiguo_nombre, antiguo_precio)
            producto_modificado = True
        elif nuevo_nombre == '' and nuevo_precio != '':
            parametros = (antiguo_nombre, nuevo_precio, antiguo_nombre, antiguo_precio)
            producto_modificado = True

        if(producto_modificado):
            self.db_consulta(query,parametros)
            self.ventana_editar.destroy()
            self.mensaje["text"] = "El producto {} ha sido actualizado con éxito".format(antiguo_nombre)
            self.mensaje["fg"] = "green"
            self.get_productos()
        else:
            self.ventana_editar.destroy()
            self.mensaje["text"] = "ERROR".format(antiguo_nombre)

    def mensaje_eliminar(self):
        nombre = self.tabla.item(self.tabla.selection())["text"]
        old_precio = self.tabla.item(self.tabla.selection())["values"][0]

        # ventana nueva (Mensaje eliminar producto)
        self.ventana_mensaje_eliminar = Toplevel()  # creacion de una ventana
        self.ventana_mensaje_eliminar.title = "Eliminar producto seleccionado"
        self.ventana_mensaje_eliminar.resizable(1, 1)

        titulo = Label(self.ventana_mensaje_eliminar, text="Eliminar producto",anchor= E,font=("Calibri", 16,"bold"))
        titulo.grid(row=0,column=2)

        # Creación del contenedor frame de la ventana mensaje_eliminar
        frame_el = LabelFrame( self.ventana_mensaje_eliminar, text="Estas apunto de eliminar el siguiente producto:", font=("Calibri", 13,"bold"))
        frame_el.grid( row=4, column=0, columnspan=5, pady=5)

        # label nombre del producto
        self.nombre_producto = Label(frame_el, text="Nombre del producto : ", font=('Calibri', 13))
        self.nombre_producto.grid(row=5, column=0)
        # Entry nombre del producto
        self.input_nombre_producto = Entry(frame_el, textvariable=StringVar(self.ventana_mensaje_eliminar,value=nombre), state="readonly",font=("Calibri", 13))
        self.input_nombre_producto.grid(row=5,column=1)

        # Label precio
        self.precio_producto = Label(frame_el, text="Precio: ", font=('Calibri', 13))
        self.precio_producto.grid(row=6,column=0)
        self.input_precio_producto = Entry(frame_el, textvariable=StringVar(self.ventana_mensaje_eliminar, value=old_precio), state= "readonly", font=("Calibri",13))
        self.input_precio_producto.grid(row=6, column=1)



        # Boton eliminar y cancelar
        self.boton_eliminar2 = ttk.Button(frame_el,text="ELIMINAR", style="eliminar.TButton", command=self.del_producto)
        self.boton_eliminar2.grid(row=8,column=0, sticky=W + E)
        self.boton_cancelar = ttk.Button(frame_el, text="CANCELAR",style="my.TButton",command=self.ventana_mensaje_eliminar.destroy)
        self.boton_cancelar.grid(row=8,column=1, sticky=W + E)




    def mensaje_prueba(self):
        # Comprobacion de que se seleccione un producto para poder eliminarlo
        self.mensaje["text"] = ""
        try:
            self.tabla.item(self.tabla.selection())["text"][0]
        except IndexError as e:
            self.mensaje["text"] = "Por favor, seleccione un producto"

        nombre = self.tabla.item(self.tabla.selection())["text"]
        old_precio = self.tabla.item(self.tabla.selection())["values"][0]
        resultado=MessageBox.askquestion("ELIMINAR",
                                       "¿Está seguro que desea eliminar el producto {} ?".format(self.nombre.get()))

        if resultado == "yes":
            self.del_producto()
            self.get_productos()































