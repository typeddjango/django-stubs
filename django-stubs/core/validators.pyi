from collections.abc import Callable, Collection, Sequence, Sized
from decimal import Decimal
from re import Pattern, RegexFlag
from typing import Any

from django.core.files.base import File
from django.utils.functional import _StrPromise
from typing_extensions import TypeAlias

EMPTY_VALUES: Any

_Regex: TypeAlias = str | Pattern[str]

_ValidatorCallable: TypeAlias = Callable[[Any], None]

class RegexValidator:
    regex: _Regex  # Pattern[str] on instance, but may be str on class definition
    message: str | _StrPromise
    code: str
    inverse_match: bool
    flags: int
    def __init__(
        self,
        regex: _Regex | None = ...,
        message: str | _StrPromise | None = ...,
        code: str | None = ...,
        inverse_match: bool | None = ...,
        flags: RegexFlag | None = ...,
    ) -> None: ...
    def __call__(self, value: Any) -> None: ...

class URLValidator(RegexValidator):
    ul: str
    ipv4_re: str
    ipv6_re: str
    hostname_re: str
    domain_re: str
    tld_re: str
    host_re: str
    schemes: Sequence[str]
    def __init__(self, schemes: Sequence[str] | None = ..., **kwargs: Any) -> None: ...
    def __call__(self, value: str) -> None: ...

integer_validator: RegexValidator

def validate_integer(value: float | str | None) -> None: ...

class EmailValidator:
    message: str
    code: str
    user_regex: Pattern[str]
    domain_regex: Pattern[str]
    literal_regex: Pattern[str]
    domain_allowlist: Sequence[str]
    def __init__(
        self,
        message: str | None = ...,
        code: str | None = ...,
        allowlist: Sequence[str] | None = ...,
        *,
        whitelist: Sequence[str] | None = ...,
    ) -> None: ...
    @property
    def domain_whitelist(self) -> Sequence[str]: ...
    @domain_whitelist.setter
    def domain_whitelist(self, allowlist: Sequence[str]) -> None: ...
    def __call__(self, value: str | None) -> None: ...
    def validate_domain_part(self, domain_part: str) -> bool: ...
    def __eq__(self, other: Any) -> bool: ...

validate_email: EmailValidator
slug_re: Pattern[str]
validate_slug: RegexValidator
slug_unicode_re: Pattern[str]
validate_unicode_slug: RegexValidator

def validate_ipv4_address(value: str) -> None: ...
def validate_ipv6_address(value: str) -> None: ...
def validate_ipv46_address(value: str) -> None: ...

_IPValidator: TypeAlias = tuple[list[Callable[[Any], None]], str]
ip_address_validator_map: dict[str, _IPValidator]

def ip_address_validators(protocol: str, unpack_ipv4: bool) -> _IPValidator: ...
def int_list_validator(
    sep: str = ..., message: str | None = ..., code: str = ..., allow_negative: bool = ...
) -> RegexValidator: ...

validate_comma_separated_integer_list: RegexValidator

class BaseValidator:
    message: str
    code: str
    limit_value: Any
    def __init__(self, limit_value: Any, message: str | None = ...) -> None: ...
    def __call__(self, value: Any) -> None: ...
    def compare(self, a: Any, b: Any) -> bool: ...
    def clean(self, x: Any) -> Any: ...
    def __eq__(self, other: Any) -> bool: ...

class MaxValueValidator(BaseValidator):
    message: str
    code: str
    def compare(self, a: Any, b: Any) -> bool: ...

class MinValueValidator(BaseValidator):
    message: str
    code: str
    def compare(self, a: Any, b: Any) -> bool: ...

class MinLengthValidator(BaseValidator):
    message: str
    code: str
    def compare(self, a: Any, b: Any) -> bool: ...
    def clean(self, x: Sized) -> int: ...

class MaxLengthValidator(BaseValidator):
    message: str
    code: str
    def compare(self, a: Any, b: Any) -> bool: ...
    def clean(self, x: Sized) -> int: ...

class DecimalValidator:
    messages: dict[str, str]
    max_digits: int | None
    decimal_places: int | None
    def __init__(self, max_digits: int | None, decimal_places: int | None) -> None: ...
    def __call__(self, value: Decimal) -> None: ...
    def __eq__(self, other: Any) -> bool: ...

class FileExtensionValidator:
    message: str
    code: str
    allowed_extensions: Collection[str] | None
    def __init__(
        self,
        allowed_extensions: Collection[str] | None = ...,
        message: str | None = ...,
        code: str | None = ...,
    ) -> None: ...
    def __call__(self, value: File) -> None: ...

def get_available_image_extensions() -> Sequence[str]: ...
def validate_image_file_extension(value: File) -> None: ...

class ProhibitNullCharactersValidator:
    message: str
    code: str
    def __init__(self, message: str | None = ..., code: str | None = ...) -> None: ...
    def __call__(self, value: Any) -> None: ...
