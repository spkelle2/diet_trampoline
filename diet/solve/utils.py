"""
Utilities to be used in conjuction with the diet package
"""


# a custom exception that can be raised to show an error is related to diet package
class DietException(Exception):
    pass


def verify(b, msg):
    if not b:
        raise DietException(msg)