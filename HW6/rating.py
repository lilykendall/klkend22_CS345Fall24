# Group Members: Lily Kendall, Lacey Eckert, Brody Pinto
class Rating:

    # user_id is a foreign key to the users table
    # isbn is a foreign key to the books table
    def __init__(self, user_id: str, isbn: str, rating: int):
        self.user_id = user_id
        self.isbn = isbn
        self.rating = rating

    def __str__(self):
        return f"User ID: {self.user_id}, ISBN: {self.isbn}, Rating: {self.rating}"

    def __repr__(self):
        return f"Rating({self.user_id}, {self.isbn}, {self.rating})"
