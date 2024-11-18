import tkinter as tk
from tkinter import messagebox
from biblioteca import Libro, BST, ArbolNArio, AVL, GrafoLibros

class BibliotecaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Biblioteca")
        self.libros = []
        self.bst = BST()
        self.arbol_nario = ArbolNArio()
        self.avl = AVL()
        self.grafo = GrafoLibros()
        self.diccionario_autores = {}

        self.frame = tk.Frame(root)
        self.frame.pack()

        self.titulo_label = tk.Label(self.frame, text="Título")
        self.titulo_label.grid(row=0, column=0)
        self.titulo_entry = tk.Entry(self.frame)
        self.titulo_entry.grid(row=0, column=1)

        self.autor_label = tk.Label(self.frame, text="Autor")
        self.autor_label.grid(row=1, column=0)
        self.autor_entry = tk.Entry(self.frame)
        self.autor_entry.grid(row=1, column=1)

        self.genero_label = tk.Label(self.frame, text="Género")
        self.genero_label.grid(row=2, column=0)
        self.genero_entry = tk.Entry(self.frame)
        self.genero_entry.grid(row=2, column=1)

        self.ano_label = tk.Label(self.frame, text="Año de Publicación")
        self.ano_label.grid(row=3, column=0)
        self.ano_entry = tk.Entry(self.frame)
        self.ano_entry.grid(row=3, column=1)

        self.descripcion_label = tk.Label(self.frame, text="Descripción")
        self.descripcion_label.grid(row=4, column=0)
        self.descripcion_entry = tk.Entry(self.frame)
        self.descripcion_entry.grid(row=4, column=1)

        self.agregar_button = tk.Button(self.frame, text="Agregar Libro", command=self.agregar_libro)
        self.agregar_button.grid(row=5, column=0, columnspan=2)

        self.mostrar_grafo_button = tk.Button(self.frame, text="Mostrar Grafo", command=self.mostrar_grafo)
        self.mostrar_grafo_button.grid(row=6, column=0, columnspan=2)

    def agregar_libro(self):
        titulo = self.titulo_entry.get()
        autor = self.autor_entry.get()
        genero = self.genero_entry.get()
        ano_publicacion_str = self.ano_entry.get()
        
        # Validar que el año de publicación sea un número entero
        if not ano_publicacion_str.isdigit():
            messagebox.showerror("Error", "El año de publicación debe ser un número entero.")
            return
        
        ano_publicacion = int(ano_publicacion_str)
        descripcion = self.descripcion_entry.get()

        libro = Libro(titulo, autor, genero, ano_publicacion, descripcion)
        self.libros.append(libro)
        self.bst.insertar(libro)
        self.arbol_nario.agregar_libro(libro)
        self.avl.insertar(libro)
        self.grafo.agregar_libro(libro)
        if autor not in self.diccionario_autores:
            self.diccionario_autores[autor] = []
        self.diccionario_autores[autor].append(libro)

        for otro_libro in self.libros:
            if otro_libro != libro:
                self.grafo.conectar_libros(libro.titulo, otro_libro.titulo)

        messagebox.showinfo("Información", "Libro agregado exitosamente")

    def mostrar_grafo(self):
        self.grafo.mostrar_grafo()

if __name__ == "__main__":
    root = tk.Tk()
    app = BibliotecaGUI(root)
    root.mainloop()