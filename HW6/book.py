# Group Members: Lily Kendall, Lacey Eckert, Brody Pinto
# dataclass, the only job of a data class is to aggregate data and not define lots of behavior.
class Book:

    # Book constructor:
    def __init__(self, isbn: str, title: str, author: str, publication_year: int, publisher: str, url_s: str, url_m: str, url_l: str):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.publication_year = publication_year
        self.publisher = publisher
        self.url_s = url_s
        self.url_m = url_m
        self.url_l = url_l

    # return a string representation of the object
    def __str__(self):
        return f"ISBN: {self.isbn}, Title: {self.title}, Author: {self.author}, Publication Year: {self.publication_year}, Publisher: {self.publisher}, url_s: {self.url_s}, url_m: {self.url_m}, url_l: {self.url_l}"

    # return a string that can be used to recreate the object
    def __repr__(self):
        return f"Book({self.isbn}, {self.title}, {self.author}, {self.publication_year}, {self.publisher}, {self.url_s}, {self.url_m}, {self.url_l})"
