import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.ttk import Combobox
from GestionBiblioteca import Biblioteca


class BibliotecaGUI:
    def __init__(self, biblioteca):
        self.biblioteca = biblioteca
        self.root = tk.Tk()
        self.root.title("Gestión de Biblioteca")

        self.selected_book_index = None


        self.label_titulo = tk.Label(self.root, text="Título:")
        self.label_titulo.grid(row=0, column=0)
        self.entry_titulo = tk.Entry(self.root)
        self.entry_titulo.grid(row=0, column=1)

        self.label_autor = tk.Label(self.root, text="Autor:")
        self.label_autor.grid(row=1, column=0)
        self.entry_autor = tk.Entry(self.root)
        self.entry_autor.grid(row=1, column=1)

        self.label_categoria = tk.Label(self.root, text="Categoría:")
        self.label_categoria.grid(row=2, column=0)
        self.entry_categoria = Combobox(
            state="readonly",
            values=[
                "No Ficción", "Ciencia Ficción", "Fantasía", "Biografía", "Historia",
                "Misterio", "Educación", "Aventura", "Poesía"
            ]
        )
        self.entry_categoria.grid(row=2, column=1)

        self.label_ano = tk.Label(self.root, text="Año de Publicación:")
        self.label_ano.grid(row=3, column=0)
        self.entry_ano = tk.Entry(self.root)
        self.entry_ano.grid(row=3, column=1)

        self.label_isbn = tk.Label(self.root, text="ISBN:")
        self.label_isbn.grid(row=4, column=0)
        self.entry_isbn = tk.Entry(self.root)
        self.entry_isbn.grid(row=4, column=1)


        self.btn_crear = tk.Button(self.root, text="Crear Libro", command=self.crear_libro)
        self.btn_crear.grid(row=5, column=0)

        self.btn_leer = tk.Button(self.root, text="Leer Libros", command=self.leer_libros)
        self.btn_leer.grid(row=5, column=1)

        self.btn_actualizar = tk.Button(self.root, text="Actualizar Libro", command=self.actualizar_libro)
        self.btn_actualizar.grid(row=5, column=2)


        self.tree = ttk.Treeview(self.root, columns=("Titulo", "Autor", "Categoria", "Ano", "ISBN"), show="headings")
        self.tree.heading("Titulo", text="Título")
        self.tree.heading("Autor", text="Autor")
        self.tree.heading("Categoria", text="Categoría")
        self.tree.heading("Ano", text="Año de Publicación")
        self.tree.heading("ISBN", text="ISBN")

        self.tree.column("Titulo", width=150)
        self.tree.column("Autor", width=100)
        self.tree.column("Categoria", width=100)
        self.tree.column("Ano", width=50)
        self.tree.column("ISBN", width=120)

        self.tree.grid(row=6, column=0, columnspan=3)


        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def crear_libro(self):
        titulo = self.entry_titulo.get()
        autor = self.entry_autor.get()
        categoria = self.entry_categoria.get()
        ano = self.entry_ano.get()
        isbn = self.entry_isbn.get()

        if titulo and autor and categoria and ano and isbn:
            self.biblioteca.crear_libro(titulo, autor, categoria, ano, isbn)
            messagebox.showinfo("Éxito", "Libro creado exitosamente")
            self.limpiar_entradas()
            self.leer_libros()
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")

    def leer_libros(self):

        for row in self.tree.get_children():
            self.tree.delete(row)


        libros = self.biblioteca.leer_libros()
        for index, libro in enumerate(libros):
            self.tree.insert("", "end", iid=index, values=(libro.titulo, libro.autor, libro.categoria, libro.anoPublicacion, libro.isbn))

    def actualizar_libro(self):

        titulo = self.entry_titulo.get()
        autor = self.entry_autor.get()
        categoria = self.entry_categoria.get()
        ano = self.entry_ano.get()
        isbn = self.entry_isbn.get()


        if self.selected_book_index is not None:
            libro_seleccionado = self.biblioteca.leer_libros()[self.selected_book_index]


            self.biblioteca.actualizar_libro(
                isbn=libro_seleccionado.isbn,
                nuevo_titulo=titulo,
                nuevo_autor=autor,
                nueva_categoria=categoria,
                nuevo_ano_publicacion=ano
            )


            self.leer_libros()
            self.limpiar_entradas()
        else:
            messagebox.showwarning("Advertencia", "No hay libro seleccionado para actualizar")

    def on_tree_select(self, event):

        selected_item = self.tree.selection()
        if selected_item:
            self.selected_book_index = int(selected_item[0])


            libro = self.biblioteca.leer_libros()[self.selected_book_index]


            self.entry_titulo.delete(0, tk.END)
            self.entry_titulo.insert(0, libro.titulo)

            self.entry_autor.delete(0, tk.END)
            self.entry_autor.insert(0, libro.autor)

            self.entry_categoria.set(libro.categoria)

            self.entry_ano.delete(0, tk.END)
            self.entry_ano.insert(0, libro.anoPublicacion)

            self.entry_isbn.delete(0, tk.END)
            self.entry_isbn.insert(0, libro.isbn)

    def limpiar_entradas(self):

        self.entry_titulo.delete(0, tk.END)
        self.entry_autor.delete(0, tk.END)
        self.entry_categoria.set("")
        self.entry_ano.delete(0, tk.END)
        self.entry_isbn.delete(0, tk.END)
        self.selected_book_index = None

    def iniciar(self):
        self.root.mainloop()



biblioteca = Biblioteca('biblioteca.json')
gui = BibliotecaGUI(biblioteca)
gui.iniciar()