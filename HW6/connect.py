# Group Members: Lily Kendall, Lacey Eckert, Brody Pinto
import psycopg
from psycopg import Connection

# specify the Connection return type
def connect() -> Connection:

    # Connect to the database:
    try:
        conn = psycopg.connect(
            dbname = "bjpint21_klkend22_laecke22_books",
            user = "cslabtes",
            host = "ada.hpc.stlawu.edu",
            password = "cslabtes",
        )
    except psycopg.Error:
        print("Cannot connect.")
        exit(1)

    return conn


