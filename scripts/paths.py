from pathlib import Path

PROJECT_DIRECTORY = Path(__file__).parent.parent
DJANGO_SOURCE_DIRECTORY = PROJECT_DIRECTORY / "django-source"  # type: Path
STUBGEN_OUTPUT_DIRECTORY = PROJECT_DIRECTORY / "stubgen"  # type: Path


if __name__ == "__main__":
    print(DJANGO_SOURCE_DIRECTORY)
    print(STUBGEN_OUTPUT_DIRECTORY)
