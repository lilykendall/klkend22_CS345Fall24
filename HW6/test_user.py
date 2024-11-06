# Group Members: Lily Kendall, Lacey Eckert, Brody Pinto
from tabulate import tabulate
from users_queries import get_user_by_id, insert_new_user, remove_user
from connect import connect
import unittest

class UsersTests(unittest.TestCase):

    def test_insert_new_user(self):
        """
        Test the insert_new_user function
        :return: None
        """
        print('\n test_insert_new_user(conn, "1234567890", "Here", 89)')

        conn = connect()
        # Remove the user first
        remove_user(conn, "999992")
        insert_new_user(conn, "999992", "New Zealand", 99)

        user = get_user_by_id(conn, "999992")
        user.insert(0, ("User ID", "Location", "Age"))
        table = tabulate(user, headers="firstrow", tablefmt="psql")

        with open("gold/t4.txt") as f:
            expected = f.read()

        conn.close()
        self.assertEqual(expected, table)

    def test_insert_new_user_negative(self):
        """
        Test the insert_new_user function with a negative test
        :return: None
        """
        print('\n test_insert_new_user_negative(conn, "123456", "Here", 89)')

        conn = connect()

        try:
            insert_new_user(conn, "123456", "Here", 89)

        except Exception as e:
            self.assertRaises(Exception, msg="User Already Exists")

        conn.close()



if __name__ == "__main__":
    unittest.main()