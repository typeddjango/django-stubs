from argparse import ArgumentParser

from mypy.stubgen import generate_stubs, parse_options

from scripts.git_helpers import checkout_django_branch
from scripts.paths import DJANGO_SOURCE_DIRECTORY

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--django_version", required=True)
    parser.add_argument("--commit_sha", required=False)
    args = parser.parse_args()
    checkout_django_branch(args.django_version, args.commit_sha)
    stubgen_options = parse_options([f"{DJANGO_SOURCE_DIRECTORY}", "-o=stubgen"])
    generate_stubs(stubgen_options)
