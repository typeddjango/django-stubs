from pathlib import Path

from django_stubs_ext.settings import TemplatesSetting

BASE_DIR = Path(__file__).resolve().parent

# Example taken from various doc pages
# https://docs.djangoproject.com/en/5.2/ref/settings/#templates
TEMPLATES: list[TemplatesSetting] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
    },
]

# https://docs.djangoproject.com/en/5.2/ref/templates/api/#the-dirs-option
TEMPLATES_2: list[TemplatesSetting] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            "/home/html/templates/lawrence.com",
            "/home/html/templates/default",
        ],
    },
]

# https://docs.djangoproject.com/en/5.2/ref/templates/api/#template-loaders
TEMPLATES_3: list[TemplatesSetting] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
    }
]
TEMPLATES_4: list[TemplatesSetting] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "OPTIONS": {
            "loaders": [
                (
                    "django.template.loaders.filesystem.Loader",
                    [BASE_DIR / "templates"],
                ),
            ],
        },
    }
]
# https://docs.djangoproject.com/en/5.2/ref/templates/api/#django.template.loaders.cached.Loader
TEMPLATES_5: list[TemplatesSetting] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "OPTIONS": {
            "loaders": [
                (
                    "django.template.loaders.cached.Loader",
                    [
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                        "path.to.custom.Loader",
                    ],
                ),
            ],
        },
    }
]
# https://docs.djangoproject.com/en/5.2/ref/templates/api/#django.template.loaders.cached.Loader
TEMPLATES_6: list[TemplatesSetting] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "OPTIONS": {
            "loaders": [
                (
                    "django.template.loaders.locmem.Loader",
                    {
                        "index.html": "content here",
                    },
                ),
            ],
        },
    }
]
# https://docs.djangoproject.com/en/5.2/topics/templates/#configuration
TEMPLATES_7: list[TemplatesSetting] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            # ... some options here ...
        },
    },
]
# https://docs.djangoproject.com/en/5.2/topics/templates/#django.template.backends.base.Template.render
TEMPLATES_8: list[TemplatesSetting] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            "/home/html/example.com",
            "/home/html/default",
        ],
    },
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "DIRS": [
            "/home/html/jinja2",
        ],
    },
]

# Custom jinja backend
TEMPLATES_9: list[TemplatesSetting] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates" / "django"],
        "APP_DIRS": True,
    },
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "DIRS": [BASE_DIR / "templates" / "jinja"],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "environment": "example.jinja.environment",
            "extensions": [
                "jinja2.ext.do",
                "jinja2.ext.i18n",
                "jinja2.ext.loopcontrols",
            ],
        },
    },
]
