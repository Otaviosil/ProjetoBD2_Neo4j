from database import Database
from movie import Movie

class MovieCRUD:
    def __init__(self):
        """
        Inicializa a conexão com o banco de dados.
        """
        self.db = Database("neo4j+s://13e81806.databases.neo4j.io", "neo4j", "bssVujeJyyuPUd5GC42_DS9mPYGsimmoPEmRoch1RPw")

    def close(self):
        """
        Encerra a conexão com o banco de dados.
        """
        self.db.close()

    def create(self, movie: Movie):
        """
        Cria um novo filme no banco de dados.

        :param movie: Objeto da classe Movie contendo os dados do filme.
        :return: O filme recém-criado.
        """
        query = """
        CREATE (m:Movie {title: $title, genre: $genre, director: $director})
        WITH m
        UNWIND $actors AS actor_name
        MERGE (a:Actor {name: actor_name})  // Garante que o nó de ator exista
        MERGE (a)-[:ACTS_IN]->(m)           // Cria o relacionamento entre o ator e o filme
        RETURN m
        """
        parameters = {
            "title": movie.title,
            "genre": movie.genre,
            "director": movie.director,
            "actors": movie.actors,
        }
        results = self.db.execute_query(query, parameters)
        return results

    def read(self, title: str) -> Movie:
        """
        Lê os detalhes de um filme no banco de dados pelo título.

        :param title: Título do filme a ser buscado.
        :return: Objeto Movie contendo os dados do filme, ou None se não encontrado.
        """
        query = """
        MATCH (m:Movie {title: $title})
        OPTIONAL MATCH (m)<-[:ACTS_IN]-(a:Actor)
        RETURN m.title AS title, m.genre AS genre, m.director AS director, COLLECT(a.name) AS actors
        """
        parameters = {"title": title}
        results = self.db.execute_query(query, parameters)

        if results:
            data = results[0]
            return Movie(
                title=data["title"],
                genre=data["genre"],
                director=data["director"],
                actors=data["actors"],
            )
        return None

    def update(self, title: str, updated_movie: Movie):
        """
        Atualiza os dados de um filme no banco de dados.

        :param title: Título atual do filme.
        :param updated_movie: Objeto Movie contendo os dados atualizados.
        :return: O filme atualizado.
        """
        query = """
        MATCH (m:Movie {title: $title})
        // Atualiza as propriedades do filme
        SET m.title = COALESCE($new_title, m.title),
            m.genre = COALESCE($new_genre, m.genre),
            m.director = COALESCE($new_director, m.director)
        // Remove todos os relacionamentos ACTS_IN com atores antigos
        WITH m
        OPTIONAL MATCH (m)<-[r:ACTS_IN]-(a:Actor)
        DELETE r
        // Cria os novos relacionamentos com atores atualizados
        WITH m
        UNWIND COALESCE($new_actors, []) AS actor_name
        MERGE (a:Actor {name: actor_name})
        MERGE (a)-[:ACTS_IN]->(m)
        RETURN m
        """
        parameters = {
            "title": title,
            "new_title": updated_movie.title,
            "new_genre": updated_movie.genre,
            "new_director": updated_movie.director,
            "new_actors": updated_movie.actors,
        }
        results = self.db.execute_query(query, parameters)
        return results

    def delete(self, title: str):
        """
        Deleta um filme do banco de dados pelo título.

        :param title: Título do filme a ser deletado.
        """
        query = """
        MATCH (m:Movie {title: $title})
        DETACH DELETE m
        """
        parameters = {"title": title}
        self.db.execute_query(query, parameters)