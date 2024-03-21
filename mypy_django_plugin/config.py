import configparser
import os
import sys
import textwrap
from functools import partial
from pathlib import Path
from typing import Any, Callable, Dict, NoReturn, Optional

if sys.version_info[:2] >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

INI_USAGE = """
(config)
...
[mypy.plugins.django-stubs]
django_settings_module = str (default: `os.getenv("DJANGO_SETTINGS_MODULE")`)
strict_settings = bool (default: true)
...
"""
TOML_USAGE = """
(config)
...
[tool.django-stubs]
django_settings_module = str (default: `os.getenv("DJANGO_SETTINGS_MODULE")`)
strict_settings = bool (default: true)
...
"""
INVALID_FILE = "mypy config file is not specified or found"
COULD_NOT_LOAD_FILE = "could not load configuration file"
MISSING_SECTION = "no section [{section}] found"
DJANGO_SETTINGS_ENV_VAR = "DJANGO_SETTINGS_MODULE"
MISSING_DJANGO_SETTINGS = f"missing required 'django_settings_module' config.\
 Either specify this config or set your `{DJANGO_SETTINGS_ENV_VAR}` env var"
INVALID_BOOL_SETTING = "invalid {key!r}: the setting must be a boolean"


def exit_with_error(msg: str, is_toml: bool = False) -> NoReturn:
    """Using mypy's argument parser, raise `SystemExit` to fail hard if validation fails.

    Considering that the plugin's startup duration is around double as long as mypy's, this aims to
    import and construct objects only when that's required - which happens once and terminates the
    run. Considering that most of the runs are successful, there's no need for this to linger in the
    global scope.
    """
    from mypy.main import CapturableArgumentParser

    handler = CapturableArgumentParser(
        prog="(django-stubs) mypy", usage=textwrap.dedent(TOML_USAGE if is_toml else INI_USAGE)
    )
    handler.error(msg)


class DjangoPluginConfig:
    __slots__ = ("django_settings_module", "strict_settings")
    django_settings_module: str
    strict_settings: bool

    def __init__(self, config_file: Optional[str]) -> None:
        if not config_file:
            exit_with_error(INVALID_FILE)

        filepath = Path(config_file)
        if not filepath.is_file():
            exit_with_error(INVALID_FILE)

        if filepath.suffix.lower() == ".toml":
            self.parse_toml_file(filepath)
        else:
            self.parse_ini_file(filepath)

    def parse_toml_file(self, filepath: Path) -> None:
        toml_exit: Callable[[str], NoReturn] = partial(exit_with_error, is_toml=True)
        try:
            with filepath.open(mode="rb") as f:
                data = tomllib.load(f)
        except (tomllib.TOMLDecodeError, OSError):
            toml_exit(COULD_NOT_LOAD_FILE)

        try:
            config: Dict[str, Any] = data["tool"]["django-stubs"]
        except KeyError:
            toml_exit(MISSING_SECTION.format(section="tool.django-stubs"))

        django_settings_module = config.get("django_settings_module") or os.getenv(DJANGO_SETTINGS_ENV_VAR)
        if not django_settings_module:
            toml_exit(MISSING_DJANGO_SETTINGS)

        self.django_settings_module = django_settings_module

        if not isinstance(self.django_settings_module, str):
            toml_exit("invalid 'django_settings_module': the setting must be a string")

        self.strict_settings = config.get("strict_settings", True)
        if not isinstance(self.strict_settings, bool):
            toml_exit(INVALID_BOOL_SETTING.format(key="strict_settings"))

    def parse_ini_file(self, filepath: Path) -> None:
        parser = configparser.ConfigParser()
        try:
            with filepath.open(encoding="utf-8") as f:
                parser.read_file(f, source=str(filepath))
        except OSError:
            exit_with_error(COULD_NOT_LOAD_FILE)

        section = "mypy.plugins.django-stubs"
        if not parser.has_section(section):
            exit_with_error(MISSING_SECTION.format(section=section))

        if parser.has_option(section, "django_settings_module"):
            django_settings_module = parser.get(section, "django_settings_module").strip("'\"")
        else:
            django_settings_module = os.getenv(DJANGO_SETTINGS_ENV_VAR, "")

        if not django_settings_module:
            exit_with_error(MISSING_DJANGO_SETTINGS)

        self.django_settings_module = django_settings_module

        try:
            self.strict_settings = parser.getboolean(section, "strict_settings", fallback=True)
        except ValueError:
            exit_with_error(INVALID_BOOL_SETTING.format(key="strict_settings"))

    def to_json(self) -> Dict[str, Any]:
        """We use this method to reset mypy cache via `report_config_data` hook."""
        return {
            "django_settings_module": self.django_settings_module,
            "strict_settings": self.strict_settings,
        }
