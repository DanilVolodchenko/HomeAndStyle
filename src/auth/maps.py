from .models.db import UserModel
from .models.dto import UserDto


def map__user_model__user_dto(user_model: UserModel) -> UserDto:
    return UserDto(
        email=user_model.email,
        role=user_model.role,
        send_email=user_model.send_email
    )
