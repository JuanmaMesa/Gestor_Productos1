from models import Producto
from tkinter import ttk
from tkinter import *



if __name__ == "__main__":
    root = Tk() # instancia de la ventana virtual
    app = Producto(root)

    root.mainloop()
