from pydantic import BaseModel, Field, field_validator
from venv import logger
from enums.roles import Roles
from typing import Optional
import pytest
pytestmark = pytest.mark.skip(reason="Учебные файлы")

class User(BaseModel):
    email: str
    fullName: str
    password: str = Field(..., min_length=8, description="пароль")
    passwordRepeat: str = Field(..., min_length=8, description="повторите пароль")
    roles: list[Roles]
    banned: Optional[bool] = None
    verified: Optional[bool] = None

    @field_validator("email")
    def check_email(cls, value: str) -> str:
        if "@" not in value:
            raise ValueError("В поле email должен присутствовать символ @")
        return value


def test_user_data(registration_user_data):
    user = User(**registration_user_data)
    assert user.email == registration_user_data["email"]
    assert user.fullName == registration_user_data["fullName"]
    assert user.password == registration_user_data["password"]
    assert user.passwordRepeat == registration_user_data["passwordRepeat"]
    assert user.roles == [Roles.USER]
    logger.info(f"{user.email=} {user.fullName=} {user.password=} {user.passwordRepeat=} {user.roles=}")

    json_data = user.model_dump_json(exclude_unset=True)
    logger.info(f"{json_data=}")

    new_user = User.model_validate_json(json_data)
    logger.info(f"{new_user}")