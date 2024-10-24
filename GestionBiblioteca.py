import Libro
import os

class Biblioteca:
    def __init__(self, archivo_persistencia):
        self.archivo_persistencia = archivo_persistencia
        self.libros = self.cargar_libros()

    def cargar_libros(self):
        libros = []
        if os.path.exists(self.archivo_persistencia):
            with open(self.archivo_persistencia, 'r') as archivo:
                for linea in archivo:
                    if linea.strip():
                        libros.append(Libro.from_string(linea))
        return libros

    def guardar_libros(self):
        with open(self.archivo_persistencia, 'w') as archivo:
            for libro in self.libros:
                archivo.write(str(libro) + "\n")

    def crear_libro(self, titulo, autor, categoria, anoPublicacion, isbn):
        nuevo_libro = Libro(titulo, autor, categoria, anoPublicacion, isbn)
        self.libros.append(nuevo_libro)
        self.guardar_libros()

    def leer_libros(self):
        return self.libros

    def actualizar_libro(self, isbn, nuevo_titulo=None, nuevo_autor=None, nueva_categoria=None, nuevo_ano_publicacion=None):
        for libro in self.libros:
            if libro.isbn == isbn:
                if nuevo_titulo:
                    libro.titulo = nuevo_titulo
                if nuevo_autor:
                    libro.autor = nuevo_autor
                if nueva_categoria:
                    libro.categoria = nueva_categoria
                if nuevo_ano_publicacion:
                    libro.ano_publicacion = nuevo_ano_publicacion
                self.guardar_libros()
                return True
        return False

    def eliminar_libro(self, isbn):
        for libro in self.libros:
            if libro.isbn == isbn:
                self.libros.remove(libro)
                self.guardar_libros()
                return True
        return False