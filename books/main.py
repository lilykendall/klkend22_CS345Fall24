from connect import connect

if __name__ == "__main__":
    conn = connect()
    print("INFO: got a connection")

    cursor = conn.execute("SELECT isbn, year, publisher FROM books WHERE lower(title)=\"the grapes of wrath\"")

    for row in cursor:
        print(row)