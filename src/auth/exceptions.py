from ..common.exceptions.exceptions import HomeAndStyleBaseException


class UserBaseException(HomeAndStyleBaseException):
    """Base auth exception."""


class UserNotFoundException(UserBaseException):
    """User not found."""


class UserAlreadyExistsException(UserBaseException):
    """User already exists."""


class PasswordException(HomeAndStyleBaseException):
    """Password exception."""
