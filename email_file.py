"""
This file contains one class,
with the purpose of removing the global variable without breaking the tests.
(Model)
"""


class Email:
    """
    Effectivly a Singleton class
    """

    string = ""

    def __init__(self, email):
        self.string = email

    def __repr__(self):
        return "The email is %s" % self.string

    def value_of(self):
        """
        Getter
        """
        return self.string

    def set_email(self, email):
        """
        Setter
        """
        self.string = email
