from database import Database
from user import User

class UserCRUD:
    def __init__(self):
        self.db = Database("neo4j+s://13e81806.databases.neo4j.io", "neo4j", "bssVujeJyyuPUd5GC42_DS9mPYGsimmoPEmRoch1RPw")

    def close(self):
        self.db.close()

    def create(self, user: User):
        query = """
        CREATE (u:User {username: $username})
        RETURN u
        """
        parameters = {"username": user.username}
        results = self.db.execute_query(query, parameters)
        return results

    def read(self, username: str) -> User:
        query = """
        MATCH (u:User {username: $username})
        RETURN u.username AS username
        """
        parameters = {"username": username}
        results = self.db.execute_query(query, parameters)

        if results:
            data = results[0]
            return User(username=data["username"])
        return None

    def update(self, username: str, updated_user: User):
        query = """
        MATCH (u:User {username: $username})
        SET u.username = COALESCE($new_username, u.username)
        RETURN u
        """
        parameters = {
            "username": username,
            "new_username": updated_user.username,
        }
        results = self.db.execute_query(query, parameters)
        return results

    def delete(self, username: str):
        query = """
        MATCH (u:User {username: $username})
        DETACH DELETE u
        """
        parameters = {"username": username}
        self.db.execute_query(query, parameters)