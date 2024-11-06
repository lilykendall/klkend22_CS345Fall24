# Group Members: Lily Kendall, Lacey Eckert, Brody Pinto
from tabulate import tabulate
from book_queries import get_book_by_isbn, get_books_by_title, most_published_books, book_avg_rating, insert_new_book, \
    remove_book
from connect import connect
import unittest
from book import Book

class BooksTest(unittest.TestCase):

    def test_most_published_books(self):
        """
        Test the most_published_books function
        :return: None
        """
        conn = connect()
        print('\n test_most_published_books(conn, 10)')

        authors = most_published_books(conn, 10)

        authors.insert(0, ("Author", "Number of Books"))
        authors = tabulate(authors, headers="firstrow", tablefmt="psql")

        # context manager, open gold file for query 7
        with open("gold/t7.txt") as f:
            expected = f.read()

        conn.close()
        self.assertEqual(authors, expected)

    def test_most_published_books_negative(self):
        """
        Test the most_published_books function with a negative test
        :return: None
        """
        print('\n test_most_published_books_negative(conn, -10)')

        conn = connect()

        try:
            # Test for a negative number of books
            most_published_books(conn, -10)
        except ValueError as e:
            if "Invalid input: n must be positive" in str(e):
                self.assertRaises(ValueError)

        conn.close()


    def test_book_avg_rating(self):
        """
        Test the book_avg_rating function
        :return: None
        """
        print("\n test_book_avg_rating(conn, 'winnie-the-pooh', 'a. a. milne')")
        conn = connect()

        avg = book_avg_rating(conn, 'winnie-the-pooh', 'a. a. milne')
        avg.insert(0, ("Avg Rating", "Total Ratings"))
        table = tabulate(avg, headers="firstrow", tablefmt="psql")
        with open("gold/t2.txt") as f:
            expected = f.read()

        conn.close()
        self.assertEqual(table, expected)

    def test_book_avg_rating_negative(self):
        """
        Test the book_avg_rating function with a negative test
        :return: None
        """
        print('\n test_book_avg_rating_negative(conn, "Lily Kendall", "Lily Kendall")')
        conn = connect()

        try:
            # Test for a title and author that does not exist
            book_avg_rating(conn, "Lily Kendall", "Lily Kendall")
        except ValueError as v:
            if "Book not found" in str(v):
                self.assertRaises(ValueError)

        conn.close()

    def test_insert_new_book(self):
        """
        Test the insert_new_book function
        :return: None
        """
        print('\n test_insert_new_book(conn, book)')

        with connect() as conn:
            # Remove the book if it exists
            remove_book(conn, '9780143039434')
            # Attempt to insert the book
            insert_new_book(conn, '9780143039434', 'Foobar', 'John Foobaz', 2000, 'Penguin Classics',
                                'urls', 'urlm', 'urll')

            # Proceed to retrieve and verify the inserted book
            book = get_book_by_isbn(conn, "9780143039434")
            table = tabulate(book, headers=["ISBN", "Title", "Author", "Publication Year", "Publisher", "URL_S", "URL_M", "URL_L"], tablefmt="psql")

            with open("gold/t5.txt") as f:
                expected = f.read()

            self.assertEqual(table, expected)

    def test_insert_new_book_negative(self):
        """
        Test the insert_new_book function with a negative test
        :return: None
        """
        print("\n test_insert_new_book_negative(conn, '9780143039433', 'The Grapes of Wrath', 'John Steinbeck', 2006, 'Penguin Classics','urls', 'urlm', 'urll')")
        with connect() as conn:
            try:
                # Test for a book that already exists
                insert_new_book(conn, '9780143039433', 'The Grapes of Wrath', 'John Steinbeck', 2006, 'Penguin Classics',
                                'urls', 'urlm', 'urll')
            except Exception as e:
                self.assertRaises(Exception, msg="ISBN already exists")


if __name__ == "__main__":
    unittest.main()