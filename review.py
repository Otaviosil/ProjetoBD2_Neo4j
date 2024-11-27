class Review:
    def __init__(self, username, movie_title, rating, review_text):
        self.username = username
        self.movie_title = movie_title
        self.rating = rating
        self.review_text = review_text

    def __repr__(self):
        return f"Review(username='{self.username}', movie_title='{self.movie_title}', rating={self.rating}, review_text='{self.review_text}')"

    def to_dict(self):
        return {
            "username": self.username,
            "movie_title": self.movie_title,
            "rating": self.rating,
            "review_text": self.review_text,
        }