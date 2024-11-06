# Group Members: Lily Kendall, Lacey Eckert, Brody Pinto
from tabulate import tabulate
from connect import connect
from ratings_queries import avg_author_ratings, top_ten_ratings, top_n_popular_books, insert_new_rating, \
    get_ratings_by_user_and_isbn, remove_rating
import unittest

class RatingsTests(unittest.TestCase):

    def test_avg_author_ratings(self):
        """
        Test the avg_author_ratings function
        :return: None
        """
        print('\n test_avg_author_ratings(conn, A. A. Milne)')

        conn = connect()
        result = avg_author_ratings(conn, "A. A. Milne")
        result.insert(0, ("Avg Rating", "Number of Books"))

        table = tabulate(result, headers="firstrow", tablefmt="psql")
        with open("gold/t1.txt") as f:
            expected = f.read()

        conn.close()
        self.assertEqual(table, expected)

    def test_avg_author_ratings_negative(self):
        """
        Test the avg_author_ratings function with a negative test
        :return: None
        """
        print('\n test_avg_author_ratings_negative(conn, Lily Kendall)')

        conn = connect()

        try:
            # Test for an author that does not exist
            avg_author_ratings(conn, "Lily Kendall")

        except ValueError as v:
            if "Author not found" in str(v):
                self.assertRaises(ValueError, msg="Author not found")

        conn.close()
    
    def test_top_ten_ratings(self):
        """
        Test the top_ten_ratings function
        :return: None
        """
        print('\n test_top_ten_ratings(conn)')

        conn = connect()
        result = top_ten_ratings(conn)
        result.insert(0, ("User ID", "Number of Ratings", "Average Rating"))

        table = tabulate(result, headers="firstrow", tablefmt="psql")
        with open("gold/t3.txt") as f:
            expected = f.read()

        conn.close()
        self.assertEqual(table, expected)


    def test_top_n_popular_books(self):
        """
        Test the top_n_popular_books function
        :return: None
        """
        print('\n test_top_n_popular_books(conn, 5)')

        conn = connect()
        result = top_n_popular_books(conn, 5)
        result.insert(0, ("Title", "Author", "Number of Ratings"))

        table = tabulate(result, headers="firstrow", tablefmt="psql")
        with open("gold/t8.txt") as f:
            expected = f.read()

        conn.close()
        self.assertEqual(table, expected)

    def test_top_n_popular_books_negative(self):
        """
        Test the top_n_popular_books function with a negative test
        :return: None
        """
        print('\n test_top_n_popular_books_negative(conn, -5)')

        conn = connect()

        try:
            # Test for a negative number of books
            top_n_popular_books(conn, -5)
        except ValueError as v:
            if "Invalid input: must be positive" in str(v):
                self.assertRaises(ValueError, msg="Invalid input: n must be positive")

        conn.close()

    def test_insert_new_rating(self):
        """
        Test the insert_new_rating function
        :return: None
        """
        print('\n test_insert_new_rating(conn, 999991,9780143039433, 5)')

        with connect() as conn:
            # Remove the rating if it exists
            remove_rating(conn, '999991', '9780143039433')
            # Attempt to insert the rating
            insert_new_rating(conn, '999991','9780143039433', 5)

            # retrieve and verify inserted rating
            rating = get_ratings_by_user_and_isbn(conn, '999991','9780143039433')
            rating.insert(0, ("User ID", "ISBN", "Rating"))
            table = tabulate(rating, headers="firstrow", tablefmt="psql")

            with open("gold/t6.txt") as f:
                expected = f.read()

            self.assertEqual(table, expected)

    def test_insert_new_rating_negative(self):
        """
        Test the insert_new_rating function with a negative test
        :return: None
        """
        print("\n test_insert_new_rating_negative(conn, '999991','9780143039433', 5)")
        with connect() as conn:
            try:
                # Test for a rating that already exists
                insert_new_rating(conn, '999991','9780143039433', 5)
            except Exception as e:
                self.assertRaises(Exception, msg="Rating already exists")

if __name__ == "__main__":
    unittest.main()





