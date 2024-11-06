# Group Members: Lily Kendall, Lacey Eckert, Brody Pinto
class User:

    # User constructor:
    def __init__(self, user_id: str, location: str, age: int):
        self.user_id = user_id
        self.location = location
        self.age = age

    def __str__(self):
        return f"User ID: {self.user_id}, Location: {self.location}, Age: {self.age}"

    def __repr__(self):
        return f"User({self.user_id}, {self.location}, {self.age})"