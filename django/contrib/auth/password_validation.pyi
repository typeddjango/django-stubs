from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from pathlib import PosixPath
from typing import (
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)


def _password_validators_help_text_html(password_validators: None = ...) -> str: ...


def get_default_password_validators(
) -> Union[List[UserAttributeSimilarityValidator], List[NumericPasswordValidator]]: ...


def get_password_validators(
    validator_config: List[Dict[str, str]]
) -> Union[List[UserAttributeSimilarityValidator], List[NumericPasswordValidator]]: ...


def password_changed(
    password: str,
    user: AbstractBaseUser = ...,
    password_validators: None = ...
) -> None: ...


def password_validators_help_texts(password_validators: None = ...) -> List[str]: ...


def validate_password(
    password: str,
    user: Optional[User] = ...,
    password_validators: None = ...
) -> None: ...


class CommonPasswordValidator:
    def __init__(self, password_list_path: PosixPath = ...) -> None: ...
    def validate(self, password: str, user: None = ...) -> None: ...


class MinimumLengthValidator:
    def __init__(self, min_length: int = ...) -> None: ...
    def get_help_text(self) -> str: ...
    def validate(self, password: str, user: None = ...) -> None: ...


class NumericPasswordValidator:
    def validate(self, password: str, user: User = ...) -> None: ...


class UserAttributeSimilarityValidator:
    def __init__(self, user_attributes: Tuple[str, str, str, str] = ..., max_similarity: float = ...) -> None: ...
    def get_help_text(self) -> str: ...
    def validate(self, password: str, user: None = ...) -> None: ...