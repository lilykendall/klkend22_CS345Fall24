# Group Members: Lily Kendall, Lacey Eckert, Brody Pinto
from typing import List, Tuple
from numpy import integer
from psycopg import Connection
from rating import Rating

def get_ratings_by_user_and_isbn(conn: Connection, user_id: str, isbn: str) -> list[Tuple[str, str, int]]:
    """
    Get a list of ratings for a user
    :param conn: the database connection
    :param user_id: user ID we are looking for
    :param isbn: ISBN we are looking for
    :return: a list of ratings
    """

    query = """
        SELECT user_id, isbn, book_rating
        FROM ratings
        WHERE user_id = %s and isbn = %s;
    """

    cursor = conn.execute(query, (user_id,isbn))

    rs = []
    for row in cursor:
        rs.append((row[0], row[1], row[2]))

    return rs

# Query 1
def avg_author_ratings(conn: Connection, author: str) -> List[Tuple[float, integer]]:
    """
    Find an author's average book rating.
    Output is (Avg Rating, #books).
    Input is author name.
    :param conn: the database connection
    :param author: the author we are looking for
    :return: tuple including average rating and number of books for that author appearing in the reviews
    """

    # Helper function to clean the author name
    def get_author_cleaned(author_name):
        return author_name.replace(".", "%").replace(" ", "%")

    def reverse_author_name(author_name):
        # Split the name by spaces
        parts = author_name.strip().split()
        if len(parts) > 1:
            # Assume the last part is the last name, and the rest are initials or first/middle names
            last_name = parts[-1]
            first_and_middle = parts[:-1]
            # Join the reversed name in "Last First Middle" format
            author_name = f"{last_name} {' '.join(first_and_middle)}"
        return author_name

    query = """
        SELECT ROUND(AVG(book_rating), 3) AS avg_rating, COUNT(*) AS num_books
        FROM books
        JOIN ratings USING (isbn)
        WHERE LOWER(author) LIKE LOWER(%s)
        OR LOWER(author) LIKE LOWER(%s);
    """

    # Execute the query with both formats
    cursor = conn.execute(query, (get_author_cleaned(author), get_author_cleaned(reverse_author_name(author))))

    rs = []
    for row in cursor:

        if row[0] is None:
            raise ValueError("Author not found")

        rs.append((row[0], row[1]))

    return rs

# Query 3
def top_ten_ratings(conn: Connection) -> List[Tuple[str, integer, float]]:
    """
    Find the average rating for the top ten users that have the most book reviews.
    Output schema is ID, #ratings, avg rating. Order by number of reviews descending.
    :return: a table of the top ten users with the most book reviews, including their user ID, number of ratings, and average rating
    """

    query = """
        SELECT user_id, COUNT(*) as num_ratings, ROUND(AVG(book_rating), 3) as avg_rating
        FROM ratings
        GROUP BY user_id
        ORDER BY num_ratings DESC
        LIMIT 10;
    """

    cursor = conn.execute(query)



    rs = []
    for row in cursor:
        rs.append((row[0], row[1], row[2]))

    return rs

# Query 8
def top_n_popular_books(conn: Connection, n: int) -> List[Tuple[str, str, int]]:
    """
    What are the top n most popular books by number of ratings.
    Input is n.
    Output is n rows of title, author, number of ratings.
    What should we order by?
    :param conn: the database connection
    :param n: the number of books
    :return: a list of tuples including title, author, and number of ratings for the top n most popular books
    """

    if n < 0:
        raise ValueError("Invalid input: n must be positive")


    query = """
    SELECT title, author, COUNT(*) as num_ratings
    FROM books JOIN ratings USING (isbn)
    GROUP BY title, author
    ORDER BY num_ratings DESC
    LIMIT %s;
    """

    cursor = conn.execute(query, (n,))

    # the result set
    rs = []
    for row in cursor:


        rs.append((row[0], row[1], row[2]))

    return rs

# Query 6
def insert_new_rating(conn: Connection, user_id: str, isbn: str, rating: int) -> None:
    """
    Insert a new rating.
    Add a test to make sure that a rating was inserted.
    Add a negative test also.
    :param conn: the database connection
    :param isbn: the isbn of the book the user is rating
    :param user_id: the user_id of the user rating the book
    :param rating: the new book_rating the user is adding
    :return: None
    """

    query = """
        INSERT INTO ratings (user_id, isbn, book_rating)
        VALUES (%s, %s, %s);
    """

    check = """
        SELECT user_id, isbn
        FROM ratings
        WHERE user_id = %s AND isbn = %s;
    """

    cursor = conn.execute(check, (user_id, isbn)).fetchone()

    if cursor is None:
        conn.execute(query, (user_id, isbn, rating))
        conn.commit()
    else:
        conn.rollback()
        raise Exception("Rating (user_id, isbn) already exists")


def remove_rating(conn: Connection, user_id: str, isbn: str) -> None:
    """
    Remove a rating.
    Add a test to make sure that a rating was removed.
    Add a negative test also.
    :param conn: the database connection
    :param isbn: the isbn of the book the user is rating
    :param user_id: the user_id of the user rating the book
    :return: None
    """

    query = """
        DELETE FROM ratings
        WHERE user_id = %s AND isbn = %s;
    """

    conn.execute(query, (user_id, isbn))
    conn.commit()

