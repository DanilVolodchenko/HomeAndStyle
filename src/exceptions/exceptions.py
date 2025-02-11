class BaseDBException(Exception):
    pass


class NoDatabaseException(BaseDBException):
    """No database."""
