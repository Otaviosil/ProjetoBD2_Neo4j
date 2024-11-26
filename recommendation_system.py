from database import Database

class RecommendationSystem:
    def __init__(self):
        self.db = Database("neo4j+s://13e81806.databases.neo4j.io", "neo4j", "bssVujeJyyuPUd5GC42_DS9mPYGsimmoPEmRoch1RPw")

    def close(self):
        self.db.close()

    def recommend_by_actor(self, actor_name):
        query = """
        MATCH (a:Actor {name: $actor_name})-[:ACTS_IN]->(m:Movie)
        RETURN m.title AS title, m.genre AS genre, m.director AS director
        """
        parameters = {"actor_name": actor_name}
        results = self.db.execute_query(query, parameters)
        
        if not results:
            return f"Nenhum filme encontrado para o ator: {actor_name}"
        
        return [f"Título: {record['title']}, Gênero: {record['genre']}, Diretor: {record['director']}" for record in results]

    def recommend_by_genre(self, genre):
        query = """
        MATCH (m:Movie {genre: $genre})
        RETURN m.title AS title, m.genre AS genre, m.director AS director
        """
        parameters = {"genre": genre}
        results = self.db.execute_query(query, parameters)
        return results

    def recommend_by_director(self, director_name):
        query = """
        MATCH (m:Movie {director: $director_name})
        RETURN m.title AS title, m.genre AS genre, m.director AS director
        """
        parameters = {"director_name": director_name}
        results = self.db.execute_query(query, parameters)
        return results