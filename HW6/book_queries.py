# Group Members: Lily Kendall, Lacey Eckert, Brody Pinto
from psycopg import Connection
from typing import List,Tuple

from tabulate import tabulate

from book import Book

# Queries that operate just on the books table

def get_books_by_title(conn: Connection, title: str, limit = 3) -> List[Book]:
    """
    Return a list of books based on the title.
    :param limit: by default, only the first three books are returned, unless otherwise specified
    :param conn: Connection - a database connection
    :param title: str - the title of book
    :return: a list of books
    """

    query = """
        SELECT isbn, title, author, publication_year, publisher, url_s, url_m, url_l
        FROM books
        WHERE lower(title) = lower(%s)
        ORDER BY publication_year
        LIMIT %s
    """

    cursor = conn.execute(query, (title, limit))

    # the result set
    rs = []

    for row in cursor:
        rs.append(Book(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

    return rs

def get_book_by_isbn(conn: Connection, isbn: str) -> List[Tuple[str, str, str, int, str, str, str, str]]:
    """
    Return a book based on the isbn.
    :param conn: Connection - a database connection
    :param isbn: str - the isbn of the book
    :return: a book
    """

    query = """
        SELECT isbn, title, author, publication_year, publisher, url_s, url_m, url_l
        FROM books
        WHERE isbn = %s
    """

    cursor = conn.execute(query, (isbn,))

    # the result set
    rs = []

    for row in cursor:
        rs.append((row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

    return rs #tabulate(rs, headers=["ISBN", "Title", "Author", "Publication Year", "Publisher", "URL_S", "URL_M", "URL_L"], tablefmt="psql")

# Query 2
def book_avg_rating(conn: Connection, title: str, author: str) -> List[Tuple[float, int]]:
    """
    Find a book's average rating given a title and author.
    :param conn: the database connection
    :param title: the title of the book
    :param author: the author of the book
    :return: a table including average rating and number of ratings for that book
    """

    # Helper function to clean the author name
    def get_author_cleaned(author_name):
        return author_name.replace(".", "%").replace(" ", "%")

    def reverse_author_name(author_name):
        # Split the name by spaces
        parts = author_name.strip().split()
        if len(parts) >= 2:
            # Assume the last part is the last name, and the rest are initials or first/middle names
            last_name = parts[-1]
            first_and_middle = parts[:-1]
            # Join the reversed name in "Last First Middle" format
            author_name = f"{last_name} {' '.join(first_and_middle)}"
        return author_name

    query = """
        SELECT ROUND(AVG(book_rating), 3) AS avg_rating, COUNT(*) AS num_ratings
        FROM books JOIN ratings USING (isbn)
        WHERE LOWER(books.title) = LOWER(%s) AND (LOWER(books.author) LIKE LOWER(%s) OR LOWER(books.author) LIKE LOWER(%s));
    """

    cursor = conn.execute(query, (title, get_author_cleaned(author), get_author_cleaned(reverse_author_name(author))))

    # the result set
    rs = []
    for row in cursor:

        if row[0] is None:
            raise ValueError("Book not found")

        rs.append((row[0], row[1]))

    return rs

# Query 7
def most_published_books(conn, n: int) -> List[Tuple[str, int]]:
    """
    List the top n authors who have the most published books, accounting for variations in author names.
    :param conn: the database connection
    :param n: the number of authors
    :return: output is n rows of author name and number of books
    """

    if n < 0:
        raise ValueError("Invalid input: n must be positive")

    query = """
        SELECT author, COUNT(*) as num_books
        FROM books
        GROUP BY author
        ORDER BY num_books DESC
        LIMIT %s;
    """
    cursor = conn.execute(query, (n,))

    # the result set
    rs = []
    for row in cursor:

        rs.append((row[0], row[1]))

    return rs

# Query 5
def insert_new_book(conn: Connection, isbn: str, title: str, author: str, publication_year: int, publisher: str, url_s: str, url_m: str, url_l: str) -> None:
    """
    Insert a new book into the database.
    :param conn: the database connection
    :param isbn: the isbn of the book
    :param title: the title of the book
    :param author: the author of the book
    :param publication_year: the publication year of the book
    :param publisher: the publisher of the book
    :param url_s: the small url of the book image
    :param url_m: the medium url of the book image
    :param url_l: the large url of the book image
    :return: None
    """
    query = """
        INSERT INTO books (isbn, title, author, publication_year, publisher, url_s, url_m, url_l)
        VALUES (%s, %s, %s, %s, %s ,%s, %s, %s);
    """

    check = """
            SELECT isbn
            FROM books
            WHERE isbn = %s;
        """

    cursor = conn.execute(check, (isbn,)).fetchone()

    if cursor is None:
        conn.execute(query, (isbn, title, author, publication_year, publisher, url_s, url_m, url_l))
        conn.commit()
    else:
        conn.rollback()
        raise Exception("ISBN already exists")

def remove_book(conn: Connection, isbn: str) -> None:
    """
    Remove a book from the database.
    :param conn: the database connection
    :param isbn: the isbn of the book
    :return: None
    """
    query = """
        DELETE FROM books
        WHERE isbn = %s;
    """

    conn.execute(query, (isbn,))
    conn.commit()
