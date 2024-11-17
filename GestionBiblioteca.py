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

    def leer_libros(self):
        return self.libros

    def buscar_libro(self, parametro, parametro_busqueda="Titulo"):
        parametro = parametro.lower()
        libros_json = [libro.to_dict() for libro in self.libros]
        lista_ordenada = None
        coincidencias = None
        if parametro_busqueda == "Titulo":
            lista_ordenada = self._ordenamiento_mergesort(libros_json, "titulo")
            coincidencias = self._busqueda_binaria(lista_ordenada, parametro, "titulo")
        elif parametro_busqueda == "Autor":
            lista_ordenada = self._ordenamiento_mergesort(libros_json, "autor")
            coincidencias = self._busqueda_binaria(lista_ordenada, parametro, "autor")
        elif parametro_busqueda == "Categoria":
            lista_ordenada = self._ordenamiento_mergesort(libros_json, "categoria")
            coincidencias = self._busqueda_binaria(lista_ordenada, parametro, "categoria")
        elif parametro_busqueda == "Año de Publicación":
            lista_ordenada = self._ordenamiento_mergesort(libros_json, "anoPublicacion")
            coincidencias = self._busqueda_binaria(lista_ordenada, parametro, "anoPublicacion")
        elif parametro_busqueda == "ISBN":
            lista_ordenada = self._ordenamiento_mergesort(libros_json, "isbn")
            coincidencias = self._busqueda_binaria(lista_ordenada, parametro, "isbn")

        if coincidencias == -1:
            return []
        else:
            return [Libro.from_dict(lista_ordenada[coincidencias])]

    def _ordenamiento_mergesort(self, lista, parametro_ordenamiento): # O(n log n)
        if (len(lista)) <= 1:
            return lista
        else:
            medio = len(lista) // 2

            izquierda = []
            for i in range(0, medio):
                izquierda.append(lista[i])
            
            derecha = []
            for i in range(medio, len(lista)):
                derecha.append(lista[i])
            
            izquierda = self._ordenamiento_mergesort(izquierda, parametro_ordenamiento)
            derecha = self._ordenamiento_mergesort(derecha, parametro_ordenamiento)

            if izquierda[medio - 1][parametro_ordenamiento] <= derecha[0][parametro_ordenamiento]:
                izquierda += derecha
                return izquierda

            resultado = self._merge(izquierda, derecha, parametro_ordenamiento)
            return resultado

    def _merge(self, izquierda, derecha, parametro_ordenamiento):
        lista_mezclada = []

        while len(izquierda) > 0 and len(derecha) > 0:
            if izquierda[0][parametro_ordenamiento] < derecha[0][parametro_ordenamiento]:
                lista_mezclada.append(izquierda.pop(0))
            else:
                lista_mezclada.append(derecha.pop(0))
        
        if len(izquierda) > 0:
            lista_mezclada += izquierda
        
        if len(derecha) > 0:
            lista_mezclada += derecha
        
        return lista_mezclada

    def _busqueda_binaria(self, lista, buscado, parametro_busqueda): #O(log n)
        if len(buscado) == 0:
            return -1
        
        posicion = -1
        primero = 0
        ultimo = len(lista)-1

        while primero <= ultimo and posicion == -1:
            medio = (primero + ultimo) // 2

            temp_medio = lista[medio][parametro_busqueda].lower()
            if len(temp_medio) >= len(buscado) and temp_medio[:len(buscado)] == buscado:
                posicion = medio
            else:
                if buscado < temp_medio:
                    ultimo = medio-1
                else: 
                    primero = medio+1
        
        return posicion

    # def crear_libro(self, titulo, autor, categoria, anoPublicacion, isbn):
    #     nuevo_libro = Libro(titulo, autor, categoria, anoPublicacion, isbn)
    #     self.libros.append(nuevo_libro)
    #     self.guardar_libros()

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
    
