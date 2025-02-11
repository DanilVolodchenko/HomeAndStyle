from src.auth.services.interfaces import SecurityServiceInterface


class Security512Service(SecurityServiceInterface):
    def __init__(self, hash_handler) -> None:
        super().__init__(hash_handler)
