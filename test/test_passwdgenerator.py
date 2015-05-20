# coding:utf-8

import unittest
import sys
import os

path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, path)


from mole.auth import PasswordResetTokenGenerator


class TestPasswordResetTokenGenerator(unittest.TestCase):

    def setUp(self):
        class User:
            pk = 1
            password = ("$pbkdf2-sha256$20000$33sPwbjXmrO2tpby3rs3pg$7oTfwOUPL"
                        "fq8jn7zPH2FvuYx5LKSlhPdurPrzXTuKuw$$1431454876.426726"
                        )
        self.user = User()
        self.generator = PasswordResetTokenGenerator('secret')
        self.timestamp = 1432108821
        self.token = "NON28L-13cff1e2a33fb298ef37c768038e41de9be22252"

    def test_make_token(self):
        origin = self.token
        token = self.generator._make_token(self.user, self.timestamp)
        print(token)
        self.assertEqual(origin, token)

    def test_check_token(self):
        rtn = self.generator.check_token(self.user, self.token)
        self.assertTrue(rtn)

if __name__ == "__main__":
    unittest.main()
