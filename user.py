class User:
    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return f"User(username='{self.username}')"

    def to_dict(self):
        return {"username": self.username}