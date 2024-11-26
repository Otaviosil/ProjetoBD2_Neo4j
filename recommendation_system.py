from database import Database

class RecommendationSystem:
    def __init__(self):
        self.db = Database("bolt://localhost:7687", "neo4j", "password")

    def close(self):
        self.db.close()

    def recommend_by_actor(self, actor_name):
        query = """
        MATCH (a:Actor {name: $actor_name})-[:ACTS_IN]->(m:Movie)
        RETURN m.title AS title, m.genre AS genre, m.director AS director
        """
        parameters = {"actor_name": actor_name}
        results = self.db.execute_query(query, parameters)
        return results

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