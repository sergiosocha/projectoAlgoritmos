import pickle
import networkx as nx
import matplotlib.pyplot as plt
import logging

# Configuración del logging
logging.basicConfig(filename='sistema_libros.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

class NodoBST:
    def __init__(self, libro):
        self.libro = libro
        self.izquierda = None
        self.derecha = None

class BST:
    def __init__(self):
        self.raiz = None

    def insertar(self, libro):
        if self.raiz is None:
            self.raiz = NodoBST(libro)
        else:
            self._insertar(self.raiz, libro)

    def _insertar(self, nodo, libro):
        if libro.titulo < nodo.libro.titulo:
            if nodo.izquierda is None:
                nodo.izquierda = NodoBST(libro)
            else:
                self._insertar(nodo.izquierda, libro)
        else:
            if nodo.derecha is None:
                nodo.derecha = NodoBST(libro)
            else:
                self._insertar(nodo.derecha, libro)

    def buscar(self, titulo):
        return self._buscar(self.raiz, titulo)

    def _buscar(self, nodo, titulo):
        if nodo is None:
            return None
        if nodo.libro.titulo == titulo:
            return nodo.libro
        elif titulo < nodo.libro.titulo:
            return self._buscar(nodo.izquierda, titulo)
        else:
            return self._buscar(nodo.derecha, titulo)

class NodoNArio:
    def __init__(self, categoria):
        self.categoria = categoria
        self.hijos = []
        self.libros = []

class ArbolNArio:
    def __init__(self):
        self.raiz = NodoNArio("Libros")

    def agregar_libro(self, libro):
        nodo_genero = self._buscar_o_crear_genero(self.raiz, libro.categoria)
        nodo_genero.libros.append(libro)

    def _buscar_o_crear_genero(self, nodo, categoria):
        for hijo in nodo.hijos:
            if hijo.categoria == categoria:
                return hijo
        nuevo_nodo = NodoNArio(categoria)
        nodo.hijos.append(nuevo_nodo)
        return nuevo_nodo

    def buscar_por_genero(self, categoria):
        return self._buscar_genero(self.raiz, categoria)

    def _buscar_genero(self, nodo, categoria):
        if nodo.categoria == categoria:
            return nodo.libros
        for hijo in nodo.hijos:
            resultado = self._buscar_genero(hijo, categoria)
            if resultado:
                return resultado
        return None

class NodoAVL:
    def __init__(self, libro):
        self.libro = libro
        self.izquierda = None
        self.derecha = None
        self.altura = 1

class AVL:
    def __init__(self):
        self.raiz = None

    def insertar(self, libro):
        self.raiz = self._insertar(self.raiz, libro)

    def _insertar(self, nodo, libro):
        if not nodo:
            return NodoAVL(libro)
        if libro.anoPublicacion < nodo.libro.anoPublicacion:
            nodo.izquierda = self._insertar(nodo.izquierda, libro)
        else:
            nodo.derecha = self._insertar(nodo.derecha, libro)

        nodo.altura = 1 + max(self._get_altura(nodo.izquierda), self._get_altura(nodo.derecha))
        balance = self._get_balance(nodo)

        if balance > 1 and libro.anoPublicacion < nodo.izquierda.libro.anoPublicacion:
            return self._rotar_derecha(nodo)
        if balance < -1 and libro.anoPublicacion > nodo.derecha.libro.anoPublicacion:
            return self._rotar_izquierda(nodo)
        if balance > 1 and libro.anoPublicacion > nodo.izquierda.libro.anoPublicacion:
            nodo.izquierda = self._rotar_izquierda(nodo.izquierda)
            return self._rotar_derecha(nodo)
        if balance < -1 and libro.anoPublicacion < nodo.derecha.libro.anoPublicacion:
            nodo.derecha = self._rotar_derecha(nodo.derecha)
            return self._rotar_izquierda(nodo)

        return nodo

    def _rotar_izquierda(self, z):
        y = z.derecha
        T2 = y.izquierda
        y.izquierda = z
        z.derecha = T2
        z.altura = 1 + max(self._get_altura(z.izquierda), self._get_altura(z.derecha))
        y.altura = 1 + max(self._get_altura(y.izquierda), self._get_altura(y.derecha))
        return y

    def _rotar_derecha(self, z):
        y = z.izquierda
        T3 = y.derecha
        y.derecha = z
        z.izquierda = T3
        z.altura = 1 + max(self._get_altura(z.izquierda), self._get_altura(z.derecha))
        y.altura = 1 + max(self._get_altura(y.izquierda), self._get_altura(y.derecha))
        return y

    def _get_altura(self, nodo):
        if not nodo:
            return 0
        return nodo.altura

    def _get_balance(self, nodo):
        if not nodo:
            return 0
        return self._get_altura(nodo.izquierda) - self._get_altura(nodo.derecha)

    def buscar_por_ano(self, anoPublicacion):
        return self._buscar_ano(self.raiz, anoPublicacion)

    def _buscar_ano(self, nodo, anoPublicacion):
        if nodo is None:
            return None
        if nodo.libro.anoPublicacion == anoPublicacion:
            return nodo.libro
        elif anoPublicacion < nodo.libro.anoPublicacion:
            return self._buscar_ano(nodo.izquierda, anoPublicacion)
        else:
            return self._buscar_ano(nodo.derecha, anoPublicacion)

def quicksort_libros(libros, key):
    if len(libros) <= 1:
        return libros
    pivote = libros[len(libros) // 2]
    menores = [x for x in libros if getattr(x, key) < getattr(pivote, key)]
    iguales = [x for x in libros if getattr(x, key) == getattr(pivote, key)]
    mayores = [x for x in libros if getattr(x, key) > getattr(pivote, key)]
    return quicksort_libros(menores, key) + iguales + quicksort_libros(mayores, key)

def mergesort_libros(libros, key):
    if len(libros) <= 1:
        return libros
    medio = len(libros) // 2
    izquierda = mergesort_libros(libros[:medio], key)
    derecha = mergesort_libros(libros[medio:], key)
    return merge(izquierda, derecha, key)

def merge(izquierda, derecha, key):
    resultado = []
    i = j = 0
    while i < len(izquierda) and j < len(derecha):
        if getattr(izquierda[i], key) < getattr(derecha[j], key):
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1
    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])
    return resultado

class GrafoLibros:
    def __init__(self):
        self.grafo = nx.Graph()

    def agregar_libro(self, libro):
        if libro.titulo not in self.grafo:
            self.grafo.add_node(libro.titulo, autor=libro.autor, año=libro.anoPublicacion, categoria=libro.categoria)
            logging.info(f"Libro agregado: {libro}")

    def conectar_libros(self, titulo1, titulo2):
        if titulo1 in self.grafo and titulo2 in self.grafo:
            relaciones = []
            color = "gray"
            valor = ""

            if self.grafo.nodes[titulo1]["autor"] == self.grafo.nodes[titulo2]["autor"]:
                relaciones.append("Autor: " + self.grafo.nodes[titulo1]["autor"])
                color = "blue"
                valor = self.grafo.nodes[titulo1]["autor"]
            if self.grafo.nodes[titulo1]["categoria"] == self.grafo.nodes[titulo2]["categoria"]:
                relaciones.append("Género: " + self.grafo.nodes[titulo1]["categoria"])
                color = "green"
                valor = self.grafo.nodes[titulo1]["categoria"]
            if self.grafo.nodes[titulo1]["año"] == self.grafo.nodes[titulo2]["año"]:
                relaciones.append("Año: " + str(self.grafo.nodes[titulo1]["año"]))
                color = "red"
                valor = str(self.grafo.nodes[titulo1]["año"])

            if relaciones:
                self.grafo.add_edge(titulo1, titulo2, color=color, relaciones=", ".join(relaciones), valor=valor)
                logging.info(f"Relación agregada entre {titulo1} y {titulo2}: {', '.join(relaciones)}")

    def mostrar_grafo(self):
        pos = nx.spring_layout(self.grafo)
        edge_colors = [self.grafo[u][v]['color'] for u, v in self.grafo.edges]
        edge_labels = { (u, v): self.grafo[u][v].get('valor', '') for u, v in self.grafo.edges }
        nx.draw(self.grafo, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=10, font_weight="bold", edge_color=edge_colors)
        nx.draw_networkx_edge_labels(self.grafo, pos, edge_labels=edge_labels, font_size=8, font_color='black')
        plt.figtext(0.8, 0.5, "Leyenda:\nAzul: Autor\nVerde: Género\nRojo: Año de publicación", wrap=True, horizontalalignment='left', fontsize=12)
        plt.show()

    def guardar_grafo(self):
        try:
            with open('grafo.pkl', 'wb') as f:
                pickle.dump(self.grafo, f)
                logging.info("Grafo guardado exitosamente.")
        except Exception as e:
            logging.error(f"Error al guardar el grafo: {e}")

    def cargar_grafo(self):
        try:
            with open('grafo.pkl', 'rb') as f:
                self.grafo = pickle.load(f)
            logging.info("Grafo cargado exitosamente.")
        except FileNotFoundError:
            self.grafo = nx.Graph()
            logging.warning("No se encontró un grafo guardado, creando uno nuevo.")
