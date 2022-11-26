from argparse import ArgumentParser

from mypy.stubgen import generate_stubs, parse_options

from scripts.git_helpers import checkout_django_branch
from scripts.paths import DJANGO_SOURCE_DIRECTORY, STUBGEN_OUTPUT_DIRECTORY

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--django_version", required=True)
    parser.add_argument("--commit_sha", required=False)
    args = parser.parse_args()
    checkout_django_branch(args.django_version, args.commit_sha)
    django_root = DJANGO_SOURCE_DIRECTORY / "django"
    stubgen_options = parse_options([f"{django_root}", f"-o={STUBGEN_OUTPUT_DIRECTORY}"])
    generate_stubs(stubgen_options)
