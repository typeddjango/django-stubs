from typing import Any, Literal, overload

from django.db.models.expressions import Expression
from django.db.models.fields import (
    NOT_PROVIDED,
    CharField,
    EmailField,
    FieldInitKwargs,
    TextField,
    _GT_Char_co,
    _GT_Text_co,
    _ST_Char_contra,
    _ST_Email_contra,
    _ST_Text_contra,
)
from django.utils.functional import _StrOrPromise
from typing_extensions import Unpack, deprecated

class CICharField(CharField[_ST_Char_contra, _GT_Char_co]):
    # `CICharField()` or `CICharField(null=False)`: keeps the type var defaults.
    @overload
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = None,
        name: str | None = None,
        *,
        null: Literal[False] = False,
        db_collation: str | None = None,
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: type[NOT_PROVIDED] | Expression | Any = ...,
        **kwargs: Unpack[FieldInitKwargs[str]],
    ) -> None: ...
    # `CICharField(null=True)`: the `self` annotation gives the nullable type.
    @overload
    def __init__(
        self: CICharField[str | int | None, str | None],
        verbose_name: _StrOrPromise | None = None,
        name: str | None = None,
        *,
        null: Literal[True],
        db_collation: str | None = None,
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: type[NOT_PROVIDED] | Expression | Any = ...,
        **kwargs: Unpack[FieldInitKwargs[str]],
    ) -> None: ...
    # `Sub(null=True)` for `class Sub(CICharField): ...`: its bound types can't match the overload above.
    @overload
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = None,
        name: str | None = None,
        *,
        null: Literal[True],
        db_collation: str | None = None,
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: type[NOT_PROVIDED] | Expression | Any = ...,
        **kwargs: Unpack[FieldInitKwargs[str]],
    ) -> None: ...
    # `CICharField(null=flag)` with `flag: bool`. Stays last, as `bool` also matches `True`.
    @overload
    @deprecated("`null` must be a literal `True` or `False` for the field type to be inferred")
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = None,
        name: str | None = None,
        *,
        null: bool,
        db_collation: str | None = None,
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: type[NOT_PROVIDED] | Expression | Any = ...,
        **kwargs: Unpack[FieldInitKwargs[str]],
    ) -> None: ...

class CIEmailField(EmailField[_ST_Email_contra, _GT_Char_co]):
    # `CIEmailField()` or `CIEmailField(null=False)`: keeps the type var defaults.
    @overload
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = None,
        name: str | None = None,
        *,
        null: Literal[False] = False,
        db_collation: str | None = None,
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: type[NOT_PROVIDED] | Expression | Any = ...,
        **kwargs: Unpack[FieldInitKwargs[str]],
    ) -> None: ...
    # `CIEmailField(null=True)`: the `self` annotation gives the nullable type.
    @overload
    def __init__(
        self: CIEmailField[str | None, str | None],
        verbose_name: _StrOrPromise | None = None,
        name: str | None = None,
        *,
        null: Literal[True],
        db_collation: str | None = None,
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: type[NOT_PROVIDED] | Expression | Any = ...,
        **kwargs: Unpack[FieldInitKwargs[str]],
    ) -> None: ...
    # `Sub(null=True)` for `class Sub(CIEmailField): ...`: its bound types can't match the overload above.
    @overload
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = None,
        name: str | None = None,
        *,
        null: Literal[True],
        db_collation: str | None = None,
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: type[NOT_PROVIDED] | Expression | Any = ...,
        **kwargs: Unpack[FieldInitKwargs[str]],
    ) -> None: ...
    # `CIEmailField(null=flag)` with `flag: bool`. Stays last, as `bool` also matches `True`.
    @overload
    @deprecated("`null` must be a literal `True` or `False` for the field type to be inferred")
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = None,
        name: str | None = None,
        *,
        null: bool,
        db_collation: str | None = None,
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: type[NOT_PROVIDED] | Expression | Any = ...,
        **kwargs: Unpack[FieldInitKwargs[str]],
    ) -> None: ...

class CITextField(TextField[_ST_Text_contra, _GT_Text_co]):
    # `CITextField()` or `CITextField(null=False)`: keeps the type var defaults.
    @overload
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = None,
        name: str | None = None,
        *,
        null: Literal[False] = False,
        db_collation: str | None = None,
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: type[NOT_PROVIDED] | Expression | Any = ...,
        **kwargs: Unpack[FieldInitKwargs[str]],
    ) -> None: ...
    # `CITextField(null=True)`: the `self` annotation gives the nullable type.
    @overload
    def __init__(
        self: CITextField[str | None, str | None],
        verbose_name: _StrOrPromise | None = None,
        name: str | None = None,
        *,
        null: Literal[True],
        db_collation: str | None = None,
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: type[NOT_PROVIDED] | Expression | Any = ...,
        **kwargs: Unpack[FieldInitKwargs[str]],
    ) -> None: ...
    # `Sub(null=True)` for `class Sub(CITextField): ...`: its bound types can't match the overload above.
    @overload
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = None,
        name: str | None = None,
        *,
        null: Literal[True],
        db_collation: str | None = None,
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: type[NOT_PROVIDED] | Expression | Any = ...,
        **kwargs: Unpack[FieldInitKwargs[str]],
    ) -> None: ...
    # `CITextField(null=flag)` with `flag: bool`. Stays last, as `bool` also matches `True`.
    @overload
    @deprecated("`null` must be a literal `True` or `False` for the field type to be inferred")
    def __init__(
        self,
        verbose_name: _StrOrPromise | None = None,
        name: str | None = None,
        *,
        null: bool,
        db_collation: str | None = None,
        primary_key: bool = False,
        max_length: int | None = None,
        db_default: type[NOT_PROVIDED] | Expression | Any = ...,
        **kwargs: Unpack[FieldInitKwargs[str]],
    ) -> None: ...

__all__ = ["CICharField", "CIEmailField", "CITextField"]
