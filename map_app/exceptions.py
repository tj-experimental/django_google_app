class InvalidCredentialException(BaseException):
    """Raise exception when credentials is None or Invalid"""
    pass


class RequestNotFoundException(BaseException):
    """Raise an exception if the request object is not found."""
