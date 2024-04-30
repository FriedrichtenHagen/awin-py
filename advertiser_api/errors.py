"""
types of errors specified by awin-py
"""

from requests import Response

class AwinError(Exception):
    """A generic error caused by awin-py"""

class MissingCredentialsError(AwinError):
    """you are missing some strictly required credentials"""
