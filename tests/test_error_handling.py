import os
import tempfile
import uuid
from contextlib import contextmanager
from typing import Any, Generator, List, Optional
from unittest import mock

import pytest

from mypy_django_plugin.config import DjangoPluginConfig

TEMPLATE = """
(config)
...
[mypy.plugins.django-stubs]
django_settings_module = str (default: `os.getenv("DJANGO_SETTINGS_MODULE")`)
strict_settings = bool (default: true)
...
(django-stubs) mypy: error: {}
"""

TEMPLATE_TOML = """
(config)
...
[tool.django-stubs]
django_settings_module = str (default: `os.getenv("DJANGO_SETTINGS_MODULE")`)
strict_settings = bool (default: true)
...
(django-stubs) mypy: error: {}
"""


@contextmanager
def write_to_file(file_contents: str, suffix: Optional[str] = None) -> Generator[str, None, None]:
    with tempfile.NamedTemporaryFile(mode="w+", suffix=suffix) as config_file:
        config_file.write(file_contents)
        config_file.seek(0)
        yield config_file.name


@pytest.mark.parametrize(
    ("config_file_contents", "message_part"),
    [
        pytest.param(
            ["[not-really-django-stubs]"],
            "no section [mypy.plugins.django-stubs] found",
            id="missing-section",
        ),
        pytest.param(
            ["[mypy.plugins.django-stubs]", "\tnot_django_not_settings_module = badbadmodule"],
            "missing required 'django_settings_module' config.\
 Either specify this config or set your `DJANGO_SETTINGS_MODULE` env var",
            id="missing-settings-module",
        ),
        pytest.param(
            ["[mypy.plugins.django-stubs]"],
            "missing required 'django_settings_module' config.\
 Either specify this config or set your `DJANGO_SETTINGS_MODULE` env var",
            id="no-settings-given",
        ),
        pytest.param(
            ["[mypy.plugins.django-stubs]", "django_settings_module = some.module", "strict_settings = bad"],
            "invalid 'strict_settings': the setting must be a boolean",
            id="missing-settings-module",
        ),
    ],
)
def test_misconfiguration_handling(capsys: Any, config_file_contents: List[str], message_part: str) -> None:
    """Invalid configuration raises `SystemExit` with a precise error message."""
    contents = "\n".join(config_file_contents).expandtabs(4)
    with write_to_file(contents) as filename:
        with pytest.raises(SystemExit, match="2"):
            DjangoPluginConfig(filename)

    error_message = "usage: " + TEMPLATE.format(message_part)
    assert error_message == capsys.readouterr().err


@pytest.mark.parametrize(
    "filename",
    [
        pytest.param(uuid.uuid4().hex, id="not matching an existing file"),
        pytest.param("", id="as empty string"),
        pytest.param(None, id="as none"),
    ],
)
def test_handles_filename(capsys: Any, filename: str) -> None:
    with pytest.raises(SystemExit, match="2"):
        DjangoPluginConfig(filename)

    error_message = "usage: " + TEMPLATE.format("mypy config file is not specified or found")
    assert error_message == capsys.readouterr().err


@pytest.mark.parametrize(
    ("config_file_contents", "message_part"),
    [
        pytest.param(
            """
            [tool.django-stubs]
            django_settings_module = 123
            """,
            "invalid 'django_settings_module': the setting must be a string",
            id="django_settings_module not string",
        ),
        pytest.param(
            """
            [tool.not-really-django-stubs]
            django_settings_module = "my.module"
            """,
            "no section [tool.django-stubs] found",
            id="missing django-stubs section",
        ),
        pytest.param(
            """
            [tool.django-stubs]
            not_django_not_settings_module = "badbadmodule"
            """,
            "missing required 'django_settings_module' config.\
 Either specify this config or set your `DJANGO_SETTINGS_MODULE` env var",
            id="missing django_settings_module",
        ),
        pytest.param(
            "tool.django-stubs]",
            "could not load configuration file",
            id="invalid toml",
        ),
        pytest.param(
            """
            [tool.django-stubs]
            django_settings_module = "some.module"
            strict_settings = "a"
            """,
            "invalid 'strict_settings': the setting must be a boolean",
            id="invalid strict_settings type",
        ),
    ],
)
def test_toml_misconfiguration_handling(capsys: Any, config_file_contents, message_part) -> None:
    with write_to_file(config_file_contents, suffix=".toml") as filename:
        with pytest.raises(SystemExit, match="2"):
            DjangoPluginConfig(filename)

    error_message = "usage: " + TEMPLATE_TOML.format(message_part)
    assert error_message == capsys.readouterr().err


@pytest.mark.parametrize("boolean_value", ["true", "false"])
def test_correct_toml_configuration(boolean_value: str) -> None:
    config_file_contents = f"""
    [tool.django-stubs]
    some_other_setting = "setting"
    django_settings_module = "my.module"
    strict_settings = {boolean_value}
    """

    with write_to_file(config_file_contents, suffix=".toml") as filename:
        config = DjangoPluginConfig(filename)

    assert config.django_settings_module == "my.module"
    assert config.strict_settings is (boolean_value == "true")


@pytest.mark.parametrize("boolean_value", ["true", "True", "false", "False"])
def test_correct_configuration(boolean_value) -> None:
    """Django settings module gets extracted given valid configuration."""
    config_file_contents = "\n".join(
        [
            "[mypy.plugins.django-stubs]",
            "some_other_setting = setting",
            "django_settings_module = my.module",
            f"strict_settings = {boolean_value}",
        ]
    )
    with write_to_file(config_file_contents) as filename:
        config = DjangoPluginConfig(filename)

    assert config.django_settings_module == "my.module"
    assert config.strict_settings is (boolean_value.lower() == "true")


@pytest.mark.parametrize("boolean_value", ["true", "false"])
def test_correct_toml_configuration_with_django_setting_from_env(boolean_value: str) -> None:
    config_file_contents = f"""
    [tool.django-stubs]
    some_other_setting = "setting"
    strict_settings = {boolean_value}
    """
    django_settings_env_value = "my.module"

    with write_to_file(config_file_contents, suffix=".toml") as filename:
        with mock.patch.dict(os.environ, {"DJANGO_SETTINGS_MODULE": django_settings_env_value}):
            config = DjangoPluginConfig(filename)

    assert config.django_settings_module == django_settings_env_value
    assert config.strict_settings is (boolean_value == "true")


@pytest.mark.parametrize("boolean_value", ["true", "True", "false", "False"])
def test_correct_configuration_with_django_setting_from_env(boolean_value) -> None:
    """Django settings module gets extracted given valid configuration."""
    config_file_contents = "\n".join(
        [
            "[mypy.plugins.django-stubs]",
            "some_other_setting = setting",
            f"strict_settings = {boolean_value}",
        ]
    )
    django_settings_env_value = "my.module"

    with write_to_file(config_file_contents) as filename:
        with mock.patch.dict(os.environ, {"DJANGO_SETTINGS_MODULE": django_settings_env_value}):
            config = DjangoPluginConfig(filename)

    assert config.django_settings_module == django_settings_env_value
    assert config.strict_settings is (boolean_value.lower() == "true")
