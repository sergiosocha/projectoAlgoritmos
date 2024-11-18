import pickle
import networkx as nx
import matplotlib.pyplot as plt
import logging

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

    def conectar_arbol(self, libros):
        for i in range(len(libros)):
            for j in range(len(libros)):
                if i != j:
                    self.conectar_libros(libros[i].titulo, libros[j].titulo)

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
