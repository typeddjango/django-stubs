from django.core.exceptions import ValidationError
from django.forms import BaseForm
from django.utils.functional import lazystr
from typing_extensions import assert_type

form = BaseForm()

assert_type(form.add_error(None, "error"), None)
assert_type(form.add_error("field", "error"), None)
assert_type(form.add_error(None, lazystr("error")), None)
assert_type(form.add_error("field", lazystr("error")), None)
assert_type(form.add_error(None, ValidationError("error")), None)
assert_type(form.add_error("field", ValidationError("error")), None)
assert_type(form.add_error(None, ["error"]), None)
assert_type(form.add_error("field", ["error"]), None)
assert_type(form.add_error(None, [lazystr("error")]), None)
assert_type(form.add_error("field", [lazystr("error")]), None)
assert_type(form.add_error(None, [ValidationError("error")]), None)
assert_type(form.add_error("field", [ValidationError("error")]), None)
assert_type(form.add_error(None, {"field": "error"}), None)
assert_type(form.add_error(None, {"field": lazystr("error")}), None)
assert_type(form.add_error(None, {"field": ValidationError("error")}), None)
assert_type(form.add_error(None, {"field": ["error"]}), None)
assert_type(form.add_error(None, {"field": [lazystr("error")]}), None)
assert_type(form.add_error(None, {"field": [ValidationError("error")]}), None)
assert_type(form.add_error(None, ValidationError(["error"])), None)
assert_type(form.add_error("field", ValidationError(["error"])), None)
assert_type(form.add_error(None, ValidationError({"field": "error"})), None)

form.add_error("field", {"field": "error"})  # type: ignore[call-overload]  # pyright: ignore[reportCallIssue,reportArgumentType]
form.add_error("field", {"field": lazystr("error")})  # type: ignore[call-overload]  # pyright: ignore[reportCallIssue,reportArgumentType]
form.add_error("field", {"field": ValidationError("error")})  # type: ignore[call-overload]  # pyright: ignore[reportCallIssue,reportArgumentType]
form.add_error("field", {"field": ["error"]})  # type: ignore[call-overload]  # pyright: ignore[reportCallIssue,reportArgumentType]
form.add_error("field", {"field": [lazystr("error")]})  # type: ignore[call-overload]  # pyright: ignore[reportCallIssue,reportArgumentType]
form.add_error("field", {"field": [ValidationError("error")]})  # type: ignore[call-overload]  # pyright: ignore[reportCallIssue,reportArgumentType]
