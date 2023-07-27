import unittest
from Assignment1 import User


class TestingUser(unittest.TestCase):



    def setUp(self):
        self.user = User("Kara","6/4/1951","KaraCCrowe@trashymail.com","NY","06902")

    def test_validState(self):
        # self.user.state="NY"
        result = self.user.check_state()
        self.assertEqual(result,True)  # NY is allowed, so it should return True

    def test_invalidState(self):
        self.user.state = "NJ"
        result = self.user.check_state()
        self.assertEqual(result,False)  # NJ is not allowed, so it should return False

    def test_validZip(self):
        result = self.user.check_zip()
        self.assertEqual(result,True)  # Zipcode "06902" has no consecutive numbers, so it should return True

    def test_invalidZip(self):
        self.user.zipcode = "45678"
        result = self.user.check_zip()
        self.assertEqual(result,False)  # Zipcode "45678" has consecutive numbers, so it should return False

    def test_validMonday(self):
        self.user.birthday = "06/01/2000"  # June 1st, 2000 is the first Monday, so it should return True
        result = self.user.val_weekday()
        self.assertEqual(result,True)  # June 1st, 2000 is not the first Monday, so it should return True

    def test_invalidMonday(self):
        result = self.user.val_weekday()
        self.assertEqual(result,False)

    def test_validEmail(self):
        result = self.user.check_email()
        self.assertEqual(result,True)  # Valid email, so it should return True

    def test_invalidEmail(self):
        self.user.email = "KaraCCrowe@trashymail"  # Invalid email (missing top-level domain), so it should return False
        result = self.user.check_email()
        self.assertEqual(result,False)

    def test_Above21(self):
        result = self.user.calculateAge()
        self.assertEqual(result, True)  # Birthdate is June 1st, 2000, so age is 21 or older, should return True

    def test_Below21(self):
        self.user.birthday = "8/15/2002"  # Birthdate is August 15th, 2002, so age is younger than 21, should return False
        result = self.user.calculateAge()
        self.assertEqual(result, False)