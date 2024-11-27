from database import Database
from review import Review

class ReviewCRUD:
    def __init__(self):
        self.db = Database("neo4j+s://13e81806.databases.neo4j.io", "neo4j", "bssVujeJyyuPUd5GC42_DS9mPYGsimmoPEmRoch1RPw")

    def close(self):
        self.db.close()

    def create(self, review: Review):
        query = """
        MATCH (u:User {username: $username}), (m:Movie {title: $movie_title})
        CREATE (r:Review {rating: $rating, review_text: $review_text})
        CREATE (u)-[:WROTE]->(r)
        CREATE (r)-[:REVIEWED]->(m)
        RETURN r
        """
        parameters = {
            "username": review.username,
            "movie_title": review.movie_title,
            "rating": review.rating,
            "review_text": review.review_text,
        }
        results = self.db.execute_query(query, parameters)
        return results

    def read(self, username: str, movie_title: str) -> Review:
        query = """
        MATCH (u:User {username: $username})-[:WROTE]->(r:Review)-[:REVIEWED]->(m:Movie {title: $movie_title})
        RETURN r.rating AS rating, r.review_text AS review_text
        """
        parameters = {"username": username, "movie_title": movie_title}
        results = self.db.execute_query(query, parameters)

        if results:
            data = results[0]
            return Review(username, movie_title, data["rating"], data["review_text"])
        return None

    def update(self, username: str, movie_title: str, updated_review: Review):
        query = """
        MATCH (u:User {username: $username})-[:WROTE]->(r:Review)-[:REVIEWED]->(m:Movie {title: $movie_title})
        SET r.rating = COALESCE($new_rating, r.rating),
            r.review_text = COALESCE($new_review_text, r.review_text)
        RETURN r
        """
        parameters = {
            "username": username,
            "movie_title": movie_title,
            "new_rating": updated_review.rating,
            "new_review_text": updated_review.review_text,
        }
        results = self.db.execute_query(query, parameters)
        return results

    def delete(self, username: str, movie_title: str):
        query = """
        MATCH (u:User {username: $username})-[:WROTE]->(r:Review)-[:REVIEWED]->(m:Movie {title: $movie_title})
        DETACH DELETE r
        """
        parameters = {"username": username, "movie_title": movie_title}
        self.db.execute_query(query, parameters)