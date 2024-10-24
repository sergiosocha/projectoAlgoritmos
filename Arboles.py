# Arboles adaptados a la implentación del almacenamiento de los libros en la gestión de biblioteca
from Libro import Libro

# Arbol binario para almacenamiento por titulo
class NodoBinario:
    def __init__(self, libro:Libro):
        self.libro = libro
        self.izquierda = None
        self.derecha = None

class ArbolBinario:
    def __init__(self):
        self.raiz = None

    def insertar(self, libro:Libro):
        if self.raiz is None:
            self.raiz = NodoBinario(libro)
        else:
            self.raiz = self.insertar_recursivo(libro, self.raiz)

    def insertar_recursivo(self, libro:Libro, nodo):
        if nodo is None:
            return NodoBinario(libro)
        
        if libro.titulo <= nodo.libro.titulo:
            nodo.izquierda = self.insertar_recursivo(libro, nodo.izquierda)
        else:
            nodo.derecha = self.insertar_recursivo(libro, nodo.derecha)
        
        return nodo

    def imprimir(self):
        self.imprimir_recursivo(self.raiz)

    def imprimir_recursivo(self, nodo):
        if nodo is not None:
            self.imprimir_recursivo(nodo.izquierda)
            print(f"Título: {nodo.libro.titulo}, Categoría: {nodo.libro.categoria}, Año: {nodo.libro.anoPublicacion}")
            self.imprimir_recursivo(nodo.derecha)
    
# Arbol N-ario para almacenamiento por genero
class NodoNario:
    def __init__(self, valor):
        self.valor = valor
        self.hijos = []

class ArbolNario:
    def __init__(self):
        self.raiz = NodoNario("Almacenamiento por genero/categoria.")
    
    def insertar(self, libro:Libro):
        for genero in self.raiz.hijos:
            if genero.valor == libro.categoria:
                genero.hijos.append(libro) # ** En este caso se esta guarda el libro en si y no como otro nodo para simplificar el proceso, pero esto podría cambiar si se necesitara 
                # return True
                return
        nuevo_genero = NodoNario(libro.categoria)
        nuevo_genero.hijos.append(libro) # **
        self.raiz.hijos.append(nuevo_genero)

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
        elif libro.anoPublicacion <= nodo.libro.anoPublicacion:
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
