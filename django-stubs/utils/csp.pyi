import sys

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from enum import Enum

    class ReprEnum(Enum): ...  # type: ignore[misc]
    class StrEnum(str, ReprEnum): ...  # type: ignore[misc]

class CSP(StrEnum):
    HEADER_ENFORCE = "Content-Security-Policy"
    HEADER_REPORT_ONLY = "Content-Security-Policy-Report-Only"

    NONE = "'none'"
    REPORT_SAMPLE = "'report-sample'"
    SELF = "'self'"
    STRICT_DYNAMIC = "'strict-dynamic'"
    UNSAFE_EVAL = "'unsafe-eval'"
    UNSAFE_HASHES = "'unsafe-hashes'"
    UNSAFE_INLINE = "'unsafe-inline'"
    WASM_UNSAFE_EVAL = "'wasm-unsafe-eval'"

    NONCE = "<CSP_NONCE_SENTINEL>"
