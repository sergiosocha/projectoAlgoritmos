import json

class Libro:

    def __init__(self, titulo, autor, categoria, anoPublicacion, isbn):
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.anoPublicacion = anoPublicacion
        self.isbn = isbn

    def __str__(self):
        return f"Titulo: {self.titulo}, Autor: {self.autor}, Categoria: {self.categoria}, Año: {self.anoPublicacion}, ISBN: {self.isbn}"

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "autor": self.autor,
            "categoria": self.categoria,
            "anoPublicacion": self.anoPublicacion,
            "isbn": self.isbn
        }

    @staticmethod
    def from_dict(libro_dict):
        return Libro(
            libro_dict["titulo"], 
            libro_dict["autor"], 
            libro_dict["categoria"], 
            libro_dict["anoPublicacion"], 
            libro_dict["isbn"]
        )
