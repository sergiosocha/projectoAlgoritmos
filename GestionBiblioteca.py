import json
import os

from Libro import Libro


class Biblioteca:
    def __init__(self, archivo_persistencia):
        self.archivo_persistencia = archivo_persistencia
        self.libros = self.cargar_libros()

    def cargar_libros(self):
        if os.path.exists(self.archivo_persistencia):
            with open(self.archivo_persistencia, 'r') as archivo:
                try:
                    libros_json = json.load(archivo)
                    return [Libro.from_dict(libro) for libro in libros_json]
                except json.JSONDecodeError:
                    return []
        return []

    def guardar_libros(self, libros_actualies=None):
        if libros_actualies is not None:
            self.libros = libros_actualies
        with open(self.archivo_persistencia, 'w') as archivo:
            libros_json = [libro.to_dict() for libro in self.libros]
            json.dump(libros_json, archivo, indent=4)

    # def crear_libro(self, titulo, autor, categoria, anoPublicacion, isbn):
    #     nuevo_libro = Libro(titulo, autor, categoria, anoPublicacion, isbn)
    #     self.libros.append(nuevo_libro)
    #     self.guardar_libros()

    def leer_libros(self):
        return self.libros

    # def actualizar_libro(self, isbn, nuevo_titulo=None, nuevo_autor=None, nueva_categoria=None, nuevo_ano_publicacion=None):
    #     for libro in self.libros:
    #         if libro.isbn == isbn:
    #             if nuevo_titulo:
    #                 libro.titulo = nuevo_titulo
    #             if nuevo_autor:
    #                 libro.autor = nuevo_autor
    #             if nueva_categoria:
    #                 libro.categoria = nueva_categoria
    #             if nuevo_ano_publicacion:
    #                 libro.ano_publicacion = nuevo_ano_publicacion
    #             self.guardar_libros()
    #             return True
    #     return False

    # def eliminar_libro(self, isbn):
    #     for libro in self.libros:
    #         if libro.isbn == isbn:
    #             self.libros.remove(libro)
    #             self.guardar_libros()
    #             return True
    #     return False
