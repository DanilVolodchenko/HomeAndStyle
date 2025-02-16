class BaseDBException(Exception):
    """Base db exception."""


class HomeAndStyle(Exception):
    """Base project exception."""


class NoDatabaseException(BaseDBException):
    """No database."""


class UserNotFoundException(HomeAndStyle):
    """User not found by some filter."""
