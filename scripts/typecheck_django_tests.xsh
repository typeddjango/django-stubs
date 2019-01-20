import os
if not os.path.exists('./django-sources'):
    git clone -b stable/2.1.x https://github.com/django/django.git django-sources

ignored_error_patterns = ["Need type annotation for", "already defined on", "Cannot assign to a"]
for line in $(mypy --config-file ./scripts/mypy.ini ./django-sources/tests).split('\n'):
    for pattern in ignored_error_patterns:
        if pattern in line:
            break
    else:
        print(line)