from database import Database

class MovieCRUD:
    def __init__(self):
        self.db = Database("bolt://54.209.152.201", "neo4j", "ease-art-twenties")

    def close(self):
        self.db.close()

    def create(self, title, genre, director, actors):
        query = """
        CREATE (m:Movie {title: $title, genre: $genre, director: $director})
        WITH m
        UNWIND $actors AS actor
        CREATE (a:Actor {name: actor})-[:ACTS_IN]->(m)
        RETURN m
        """
        parameters = {"title": title, "genre": genre, "director": director, "actors": actors}
        results = self.db.execute_query(query, parameters)
        return results

    def read(self, title):
        query = """
        MATCH (m:Movie {title: $title})
        OPTIONAL MATCH (m)<-[:ACTS_IN]-(a:Actor)
        RETURN m.title AS title, m.genre AS genre, m.director AS director, COLLECT(a.name) AS actors
        """
        parameters = {"title": title}
        results = self.db.execute_query(query, parameters)
        return results

    def update(self, title, new_title=None, new_genre=None, new_director=None, new_actors=None):
        query = """
        MATCH (m:Movie {title: $title})
        SET m.title = COALESCE($new_title, m.title)
        SET m.genre = COALESCE($new_genre, m.genre)
        SET m.director = COALESCE($new_director, m.director)
        WITH m
        OPTIONAL MATCH (m)<-[:ACTS_IN]-(a:Actor)
        DELETE a
        WITH m
        UNWIND $new_actors AS actor
        CREATE (a:Actor {name: actor})-[:ACTS_IN]->(m)
        RETURN m
        """
        parameters = {
            "title": title,
            "new_title": new_title,
            "new_genre": new_genre,
            "new_director": new_director,
            "new_actors": new_actors
        }
        results = self.db.execute_query(query, parameters)
        return results

    def delete(self, title):
        query = """
        MATCH (m:Movie {title: $title})
        DETACH DELETE m
        """
        parameters = {"title": title}
        self.db.execute_query(query, parameters)