import tempfile
import typing

import pytest

from mypy_django_plugin.main import extract_django_settings_module

TEMPLATE = """usage: (config)
...
[mypy.plugins.django_stubs]
    django_settings_module: str (required)
...
(django-stubs) mypy: error: 'django_settings_module' is not set: {}
"""


@pytest.mark.parametrize(
    "config_file_contents,message_part",
    [
        pytest.param(
            None,
            "mypy config file is not specified or found",
            id="missing-file",
        ),
        pytest.param(
            ["[not-really-django-stubs]"],
            "no section [mypy.plugins.django-stubs]",
            id="missing-section",
        ),
        pytest.param(
            ["[mypy.plugins.django-stubs]", "\tnot_django_not_settings_module = badbadmodule"],
            "the setting is not provided",
            id="missing-settings-module",
        ),
        pytest.param(
            ["[mypy.plugins.django-stubs]"],
            "the setting is not provided",
            id="no-settings-given",
        ),
    ],
)
def test_misconfiguration_handling(capsys, config_file_contents, message_part):
    #  type: (typing.Any, typing.List[str], str) -> None
    """Invalid configuration raises `SystemExit` with a precise error message."""
    with tempfile.NamedTemporaryFile(mode="w+") as config_file:
        if not config_file_contents:
            config_file.close()
        else:
            config_file.write("\n".join(config_file_contents).expandtabs(4))
            config_file.seek(0)

        with pytest.raises(SystemExit, match="2"):
            extract_django_settings_module(config_file.name)

    error_message = TEMPLATE.format(message_part)
    assert error_message == capsys.readouterr().err


def test_correct_configuration() -> None:
    """Django settings module gets extracted given valid configuration."""
    config_file_contents = [
        "[mypy.plugins.django-stubs]",
        "\tsome_other_setting = setting",
        "\tdjango_settings_module = my.module",
    ]
    with tempfile.NamedTemporaryFile(mode="w+") as config_file:
        config_file.write("\n".join(config_file_contents).expandtabs(4))
        config_file.seek(0)

        extracted = extract_django_settings_module(config_file.name)

    assert extracted == "my.module"
