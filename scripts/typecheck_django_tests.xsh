#!/usr/local/bin/xonsh

import os
if not os.path.exists('./django-sources'):
    git clone -b stable/2.1.x https://github.com/django/django.git django-sources

ignored_error_patterns = ["Need type annotation for"]
for line in $(mypy --config-file typecheck_tests.ini ./django-sources/tests/files).split('\n'):
    for pattern in ignored_error_patterns:
        if pattern in line:
            break
    else:
        print(line)

