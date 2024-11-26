class Movie:
    def __init__(self, title, genre, director, actors):
        """
        Inicializa um objeto Movie com os atributos fornecidos.
        
        :param title: Título do filme.
        :param genre: Gênero do filme.
        :param director: Diretor do filme.
        :param actors: Lista de atores que participam do filme.
        """
        self.title = title
        self.genre = genre
        self.director = director
        self.actors = actors

    def __repr__(self):
        """
        Representação em string para exibição do objeto.
        """
        return f"Movie(title='{self.title}', genre='{self.genre}', director='{self.director}', actors={self.actors})"

    def to_dict(self):
        """
        Converte o objeto Movie para um dicionário, útil para passar como parâmetro em queries.
        """
        return {
            "title": self.title,
            "genre": self.genre,
            "director": self.director,
            "actors": self.actors,
        }
