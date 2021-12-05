# Slighly based on https://github.com/strawberry-graphql/strawberry/blob/main/tests/pyright/utils.py

import os
import subprocess
import tempfile
from dataclasses import dataclass
from typing import List, cast

from typing_extensions import Literal

_cwd = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_bin = os.path.join(_cwd, "node_modules", ".bin", "pyright")


@dataclass
class Result:
    type: Literal["error", "info"]
    message: str
    line: int
    column: int

    @classmethod
    def from_output_line(cls, output_line: str) -> "Result":
        # an output line looks like: filename.py:11:6 - type: Message
        file_info, result = output_line.split("-", maxsplit=1)

        line, column = [int(value) for value in file_info.split(":")[1:]]
        type_, message = [value.strip() for value in result.split(":", maxsplit=1)]
        type_ = cast(Literal["error", "info"], type_)

        return cls(type=type_, message=message, line=line, column=column)


def run_pyright(code: str) -> List[Result]:
    with tempfile.NamedTemporaryFile("w", suffix=".py") as f:
        f.write(code)
        f.flush()
        result = subprocess.run([_bin, f.name], cwd=_cwd, stdout=subprocess.PIPE)

    output = result.stdout.decode("utf-8")
    results: List[Result] = []
    for line in output.splitlines():
        if line.strip().startswith(f"{f.name}:"):
            results.append(Result.from_output_line(line))

    return results
