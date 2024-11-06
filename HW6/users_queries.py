# Group Members: Lily Kendall, Lacey Eckert, Brody Pinto
from psycopg import Connection
from typing import List, Tuple
from user import User
from tabulate import tabulate

# Queries that operate just on the users table

def get_user_by_id(conn: Connection, user_id: str) -> List[Tuple[str, str, int]]:
    """
    Return a user based on the user_id.
    :param conn: Connection - a database connection
    :param user_id: str - the user_id of the user
    :return: a table of the user
    """

    query = """
        SELECT user_id, location, age
        FROM users
        WHERE user_id = %s
    """

    cursor = conn.execute(query, (user_id,))

    # the result set
    rs = []

    for row in cursor:
        rs.append((row[0], row[1], row[2]))

    return rs

# Query 4
def insert_new_user(conn: Connection, user_id: str, location: str, age: int) -> None:
    """
    Insert a new user.
    Add a test to make sure that a user was inserted.
    Add a negative test also.
    :param user_id: new user's user_id
    :param age: new user's age
    :param location: new user's location
    :param conn: the database connection
    :return: None
    """

    query = """
        INSERT INTO users(user_id, location, age) 
        VALUES (%s, %s, %s);
        """

    check = """
        SELECT user_id
        FROM users
        WHERE user_id = %s;
    """

    cursor = conn.execute(check, (user_id,)).fetchone()

    if cursor is None:
        conn.execute(query, (user_id, location, age))
        conn.commit()
    else:
        conn.rollback()
        raise Exception("User already exists")

def remove_user(conn: Connection, user_id: str) -> None:
    """
    Remove a user.
    Add a test to make sure that a user was removed.
    Add a negative test also.
    :param user_id: the user_id of the user we are removing
    :param conn: the database connection
    :return: None
    """

    query = """
        DELETE FROM users
        WHERE user_id = %s;
    """

    conn.execute(query, (user_id,))
    conn.commit()
