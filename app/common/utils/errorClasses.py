class DuplicateUserError(Exception):
    """
    Username or email is already registered.
    :param message: str
    :return: None
    """
    def __init__(self, message: str = "Username or email already exists") -> None:
        super().__init__(message)


class InvalidCredentialsError(Exception):
    """
    Invalid credentials.
    :param message: str
    :return: None
    """
    def __init__(self, message: str = "Invalid credentials") -> None:
        super().__init__(message)

class UserNotFoundError(Exception):
    """
    User not found.
    :param message: str
    :return: None
    """
    def __init__(self, message: str = "User not found") -> None:
        super().__init__(message)


class UnauthorizedAccessError(Exception):
    """
    Unauthorized.
    :param message: str
    :return: None
    """
    def __init__(self, message: str = "Unauthorized") -> None:
        super().__init__(message)
