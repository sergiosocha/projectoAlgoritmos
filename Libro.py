class Libro:

    def __init__(self, titulo, autor, categoria, anoPublicacion, isbn):
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.anoPublicacion = anoPublicacion
        self.isbn = isbn


    def __str__(self):
        return f"Titulo: {self.titulo}, Autor: {self.autor}, Categoria: {self.categoria}, Año: {self.ano_publicacion}, ISBN: {self.isbn}"


    ##Convertir los datos aun diccionario , no se usa aun ya que nse si se puede usar json
    def to_dict(self):
        return {
            "titulo": self.titulo,
            "autor": self.autor,
            "categoria": self.categoria,
            "ano_publicacion": self.ano_publicacion,
            "isbn": self.isbn
        }

    @staticmethod
    def from_string(libro_str):

        campos = libro_str.strip().split(";")
        return Libro(campos[0], campos[1], campos[2], campos[3], campos[4])