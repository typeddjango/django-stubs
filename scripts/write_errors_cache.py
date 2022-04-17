#! /usr/bin/env python3

import json
import os
import os.path
import shutil
import sys
from pathlib import Path

from compare_errors import CURRENT_DIR, ERRORS_FILE, TEMP_ERRORS_FILE, make_meta


def mtime_is_latest(mtime: int) -> bool:
    for dirname, _, files in os.walk(CURRENT_DIR):
        if dirname == ".git":
            continue
        for file in files:
            if (Path(dirname) / file).stat().st_mtime_ns > mtime:
                return False
    return True


if __name__ == "__main__":
    sys.path.insert(0, str(CURRENT_DIR))
    if TEMP_ERRORS_FILE.exists() and mtime_is_latest(TEMP_ERRORS_FILE.stat().st_mtime_ns):
        shutil.copyfile(TEMP_ERRORS_FILE, ERRORS_FILE)
    else:
        meta = make_meta()
        with open(ERRORS_FILE, "w") as errors_file:
            json.dump(meta, errors_file)
