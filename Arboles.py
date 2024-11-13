# Arboles adaptados a la implentación del almacenamiento de los libros en la gestión de biblioteca
from Libro import Libro
import copy

# Arbol binario para almacenamiento por titulo
class NodoBinario:
    def __init__(self, libro: Libro):
        self.libro = libro
        self.izquierda = None
        self.derecha = None

class ArbolBinario:
    def __init__(self, ordenarPor='titulo'):
        self.raiz = None
        self.ordenarPor = ordenarPor

        #Variables de apoyo (usadas en funciones especificas dentro de la clase)
        self.impresion = []
        self.actualizado = False
        self.padre = None

    def insertar(self, libro: Libro):
        if self.raiz is None:
            self.raiz = NodoBinario(libro)
        else:
            self.raiz = self.insertar_recursivo(libro, self.raiz)

    def insertar_recursivo(self, libro: Libro, nodo):
        if nodo is None:
            return NodoBinario(libro)

        if self.ordenarPor == "titulo":
            if libro.titulo.lower() <= nodo.libro.titulo.lower():
                nodo.izquierda = self.insertar_recursivo(libro, nodo.izquierda)
            else:
                nodo.derecha = self.insertar_recursivo(libro, nodo.derecha)
        elif self.ordenarPor == "autor":
            if libro.autor.lower() <= nodo.libro.autor.lower():
                nodo.izquierda = self.insertar_recursivo(libro, nodo.izquierda)
            else:
                nodo.derecha = self.insertar_recursivo(libro, nodo.derecha)
        else:
            self.ordenarPor = "titulo"
            nodo = self.insertar_recursivo(libro, nodo)

        return nodo
   
    def imprimir_arbol(self, root, nivel=0, prefijo="Root: "):
        if root is not None:
            print(" " * (nivel*4) + prefijo + str(root.libro.titulo))
            if root.izquierda is not None or root.derecha is not None:
                if root.izquierda is not None:
                    self.imprimir_arbol(root.izquierda, nivel + 1, "L--- ")
                else:
                    print(" " * ((nivel + 1) * 4) + "L--- None")
                if root.derecha is not None:
                    self.imprimir_arbol(root.derecha, nivel + 1, "R--- ")
                else:
                    print(" " * ((nivel + 1) * 4) + "R--- None")
   
    def imprimir(self):
        self.impresion = []
        self.imprimir_recursivo(self.raiz)
        return self.impresion

    def imprimir_recursivo(self, nodo):
        if nodo is not None:
            self.imprimir_recursivo(nodo.izquierda)
            self.impresion.append(nodo.libro)
            self.imprimir_recursivo(nodo.derecha)

    def actualizar_libro(self, isbn, nuevo_titulo=None, nuevo_autor=None, nueva_categoria=None, nuevo_ano_publicacion=None):
        nuevos_datos = {
            "isbn": isbn,
            "nuevo_titulo": nuevo_titulo,
            "nuevo_autor": nuevo_autor,
            "nueva_categoria": nueva_categoria,
            "nuevo_ano_publicacion": nuevo_ano_publicacion
        }

        self.actualizar_recursivo(self.raiz, nuevos_datos)
        self.actualizado = False

    def actualizar_recursivo(self, nodo, nuevos_datos):
        # self.imprimir_arbol(self.raiz)
        if nodo is not None:
            if nodo.libro.isbn == nuevos_datos['isbn']:
                libro_actualizado = Libro(
                    nuevos_datos['nuevo_titulo'] or nodo.libro.titulo,
                    nuevos_datos['nuevo_autor'] or nodo.libro.autor,
                    nuevos_datos['nueva_categoria'] or nodo.libro.categoria,
                    nuevos_datos['nuevo_ano_publicacion'] or nodo.libro.anoPublicacion,
                    nodo.libro.isbn
                )
                self.raiz = self.eliminar_nodo(self.raiz, nodo.libro)
                self.insertar(libro_actualizado)

                self.actualizado = True
                return

            if not self.actualizado:
                self.actualizar_recursivo(nodo.izquierda, nuevos_datos)
            if not self.actualizado:
                self.actualizar_recursivo(nodo.derecha, nuevos_datos)

    def eliminar_nodo(self, sub_arbol, libro):
        if sub_arbol is None:
            return None

        if self.ordenarPor == "titulo":
            if libro.titulo < sub_arbol.libro.titulo:
                sub_arbol.izquierda = self.eliminar_nodo(sub_arbol.izquierda, libro)
            elif libro.titulo > sub_arbol.libro.titulo:
                sub_arbol.derecha = self.eliminar_nodo(sub_arbol.derecha, libro)
            else:
                nodo_eliminar = sub_arbol
                if nodo_eliminar.derecha is None:
                    sub_arbol = nodo_eliminar.izquierda
                elif nodo_eliminar.izquierda is None:
                    sub_arbol = nodo_eliminar.derecha
                else:
                    sub_arbol = self.sucesor(nodo_eliminar)
                    nodo_eliminar = None
                
        elif self.ordenarPor == "autor":
            if libro.autor < sub_arbol.libro.autor:
                sub_arbol.izquierda = self.eliminar_nodo(sub_arbol.izquierda, libro)
            elif libro.autor > sub_arbol.libro.autor:
                sub_arbol.derecha = self.eliminar_nodo(sub_arbol.derecha, libro)
            else:
                nodo_eliminar = sub_arbol
                if nodo_eliminar.derecha is None:
                    sub_arbol = nodo_eliminar.izquierda
                elif nodo_eliminar.izquierda is None:
                    sub_arbol = nodo_eliminar.derecha
                else:
                    sub_arbol = self.sucesor(nodo_eliminar)
                    nodo_eliminar = None
        
        else:
            self.ordenarPor = "titulo"
            return self.eliminar_nodo(sub_arbol, libro)
        
        return sub_arbol
    
    def sucesor(self, antecesor):
        sucesor = antecesor
        otro = antecesor.izquierda
        while otro.derecha is not None:
            sucesor = otro
            otro = otro.derecha
        
        antecesor.libro = otro.libro
        if sucesor == antecesor:
            sucesor.izquierda = otro.izquierda
        else:
            sucesor.derecha = otro.izquierda
        
        return otro

# Arbol N-ario para almacenamiento por categoria
class NodoNario:
    def __init__(self, valor):
        self.valor = valor
        self.hijos = []

class ArbolNario:
    def __init__(self):
        self.raiz = NodoNario("Almacenamiento por categoria.")
    
    def insertar(self, libro:Libro):
        for categoria in self.raiz.hijos:
            if categoria.valor == libro.categoria:
                categoria.hijos.append(libro) # ** En este caso se esta guarda el libro en si y no como otro nodo para simplificar el proceso, pero esto podría cambiar si se necesitara 
                # return True
                return
        nuevo_genero = NodoNario(libro.categoria.capitalize())
        nuevo_genero.hijos.append(libro) # **
        self.raiz.hijos.append(nuevo_genero)
    
    def crear_libro(self, titulo, autor, categoria, anoPublicacion, isbn):
        nuevo_libro = Libro(titulo, autor, categoria, anoPublicacion, isbn)
        self.insertar(nuevo_libro)

    def imprimir(self):
        return [
            nodo_libro.libro if isinstance(nodo_libro, list) 
            else nodo_libro 
            for categoria in self.raiz.hijos for nodo_libro in categoria.hijos
        ]
    
    def actualizar_libro(self, isbn, nuevo_titulo=None, nuevo_autor=None, nueva_categoria=None, nuevo_ano_publicacion=None):
        for categoria in self.raiz.hijos:
            for libro in categoria.hijos:
                if libro.isbn == isbn:
                    libro_actualizado = Libro(
                        nuevo_titulo or libro.titulo,
                        nuevo_autor or libro.autor,
                        nueva_categoria or libro.categoria,
                        nuevo_ano_publicacion or libro.anoPublicacion,
                        isbn
                    )

                    if libro.categoria.lower() == nueva_categoria.lower():
                        categoria.hijos.append(libro_actualizado)
                    else:
                        categoria_existente = False
                        for _categoria in self.raiz.hijos:
                            if _categoria.valor.lower() == nueva_categoria.lower():
                                categoria_existente = True
                                _categoria.hijos.append(libro_actualizado)

                        if not categoria_existente:
                            self.insertar(libro_actualizado)

                    categoria.hijos.remove(libro)

                    return
                        
# ArbolAVL para almacenamiento por anio de publicacion
class NodoAVL(NodoBinario):
    def __init__(self, libro):
        super().__init__(libro)
        self.altura = 1
    
class ArbolAVL(ArbolBinario):
    def insertar(self, libro:Libro):
        if self.raiz is None:
            self.raiz = NodoAVL(libro)
        else:
            self.raiz = self.insertar_recursivo(libro, self.raiz)    

    def insertar_recursivo(self, libro:Libro, nodo):
        if nodo is None:
            return NodoAVL(libro)
        elif int(libro.anoPublicacion) <= int(nodo.libro.anoPublicacion):
            nodo.izquierda = self.insertar_recursivo(libro, nodo.izquierda)
        else:
            nodo.derecha = self.insertar_recursivo(libro, nodo.derecha)
        
        nodo.altura = max(self.altura(nodo.izquierda), self.altura(nodo.derecha)) + 1
        factor_balance = self.balance(nodo)

        if factor_balance > 1:
            if libro.anoPublicacion <= nodo.izquierda.libro.anoPublicacion:
                return self.rotar_derecha(nodo)
            else:
                nodo.izquierda = self.rotar_izquierda(nodo.izquierda)
                return self.rotar_derecha(nodo)
        
        if factor_balance < -1:
            if libro.anoPublicacion > nodo.derecha.libro.anoPublicacion:
                return self.rotar_izquierda(nodo)
            else:
                nodo.derecha = self.rotar_derecha(nodo.derecha)
                return self.rotar_izquierda(nodo)
        
        return nodo

    def altura(self, nodo):
        if nodo is None:
            return 0
        return nodo.altura
    
    def balance(self, nodo):
        if nodo is None:
            return 0
        return self.altura(nodo.izquierda) - self.altura(nodo.derecha)

    def rotar_derecha(self, y):
        x = y.izquierda
        t2 = x.derecha
        x.derecha = y
        y.izquierda = t2
        y.altura = max(self.altura(y.izquierda), self.altura(y.derecha)) + 1
        x.altura = max(self.altura(x.izquierda), self.altura(x.derecha)) + 1
        return x

    def rotar_izquierda(self, x):
        y = x.derecha
        t2 = y.izquierda
        y.izquierda = x
        x.derecha = t2
        x.altura = max(self.altura(x.izquierda), self.altura(x.derecha)) + 1
        y.altura = max(self.altura(y.izquierda), self.altura(y.derecha)) + 1
        return y
    
    def crear_libro(self, titulo, autor, categoria, anoPublicacion, isbn):
        nuevo_libro = Libro(titulo, autor, categoria, anoPublicacion, isbn)
        self.insertar(nuevo_libro)
    
    def actualizar_libro(self, isbn, nuevo_titulo=None, nuevo_autor=None, nueva_categoria=None, nuevo_ano_publicacion=None):
        nuevos_datos = {
            "isbn": isbn,
            "nuevo_titulo": nuevo_titulo,
            "nuevo_autor": nuevo_autor,
            "nueva_categoria": nueva_categoria,
            "nuevo_ano_publicacion": nuevo_ano_publicacion
        }

        self.actualizar_recursivo(self.raiz, nuevos_datos)
        self.actualizado = False

        arbol_reorganizado = ArbolAVL()
        for libro in self.imprimir():
            arbol_reorganizado.insertar(libro)
        
        self.raiz = arbol_reorganizado.raiz

    def actualizar_recursivo(self, nodo, nuevos_datos):
        if nodo is not None:
            if nodo.libro.isbn == nuevos_datos['isbn']:
                self.imprimir_arbol(self.raiz)

                libro_actualizado = Libro(
                    nuevos_datos['nuevo_titulo'] or nodo.libro.titulo,
                    nuevos_datos['nuevo_autor'] or nodo.libro.autor,
                    nuevos_datos['nueva_categoria'] or nodo.libro.categoria,
                    nuevos_datos['nuevo_ano_publicacion'] or nodo.libro.anoPublicacion,
                    nodo.libro.isbn
                )

                nodo.libro = libro_actualizado                

                self.actualizado = True
                return
            
            if not self.actualizado:
                self.actualizar_recursivo(nodo.izquierda, nuevos_datos)
            if not self.actualizado:
                self.actualizar_recursivo(nodo.derecha, nuevos_datos)
    