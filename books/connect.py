from psycopg import Connection
import psycopg

def connect() -> Connection:
    # secure coding practice: always ask what can go wrong
    pgpass_file = None  # file handle/object

    try:
        pgpass_file = open('../../.pwd')
        # p = pgpass_file.readline().strip()
    except OSError:
        print("Error: Authorization failed")
        print("Could not open credential file")
        exit(1)

    try:
        conn = psycopg.connect(
            dbname="bjpint21_klkend22_laecke22_books",
            user = "klkend22",
            hostname = "ada.hpc.stlawu.edu",
            password = pgpass_file.readline().strip()
        )
    except psycopg.Error:
        print("Cannot connect")
        exit(1)
    finally:
        pgpass_file.close()

    return conn