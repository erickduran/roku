# errors.py
"""This is the definition class for all errors in the compiler."""

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class InvalidCharacterError(Error):
    """Exception raised for errors invalid characters.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

class EmptyFileError(Error):
    """Exception raised when reading an empty file.

    Attributes:
    message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

class SyntaxError(Error):
    """Exception raised when reading syntax errors.

    Attributes:
    message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
