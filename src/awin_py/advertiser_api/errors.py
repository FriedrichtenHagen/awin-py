"""
types of errors specified by awin-py
"""
from typing import Any, Dict, Type
from requests import Response

class AwinError(Exception):
    """A generic error caused by awin-py"""

class MissingCredentialsError(AwinError):
    """you are missing some strictly required credentials"""

class AwinApiError(AwinError):
    """
    An error response from the Awin HTTP API

    :param status_code: the HTTP status code of the API response
    :param message: the error message from the Awin API
    :param error_code: the error code that is provided with the Awin API response
           (not the HTTP status code!)
    :param errors: details about the errors that are provided by the Awin API as dictionary
    :param response: the HTTP response
    """

    def __init__(self, status_code: int, error: str = None, message: str = None, response: Response = None):
        super().__init__()
        self.status_code = status_code
        self.message = message
        self.error = error
        self.response = response

    @classmethod
    def from_response(cls, response: Response):
        """
        Creates a ``AwinApiError`` from the specified HTTP response.

        :param response: a HTTP error response from Awin
        :return: a AwinApiError that matches the HTTP error
        """
        try:
            data: Dict = response.json()
            status_code = response.status_code
            error = data.get('error')
            message = data.get('description')

            return AwinApiError(
                status_code=status_code,
                error=error,
                message=message,
                response=response)
        except ValueError:
            return AwinApiError(
                status_code=response.status_code,
                message=response.text,
                response=response)

    def __str__(self):
        message = f"Request failed with HTTP status code {self.status_code}: {self.error}."
        if self.error:
            message += f" Details: {self.message}"
        return message
    
# class UnsupportedMethodError(AwinError):
#     """this method is not supported by this class (but it might be by a similar one)"""

#     def __init__(self, method: str, clazz: Type):
#         super().__init__()
#         self.method = method
#         self.clazz = clazz

#     def __str__(self):
#         return f"method '{self.method}' is not available for {self.clazz.__name__}"