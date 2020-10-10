import shutil
from typing import Optional

from git import RemoteProgress, Repo

from scripts.paths import DJANGO_SOURCE_DIRECTORY


class ProgressPrinter(RemoteProgress):
    def line_dropped(self, line: str) -> None:
        print(line)

    def update(self, op_code, cur_count, max_count=None, message=""):
        print(self._cur_line)


def checkout_django_branch(django_version: str, commit_sha: Optional[str]) -> Repo:
    branch = f"stable/{django_version}.x"
    if DJANGO_SOURCE_DIRECTORY.exists():
        shutil.rmtree(DJANGO_SOURCE_DIRECTORY)
    DJANGO_SOURCE_DIRECTORY.mkdir(exist_ok=True, parents=False)
    repo = Repo.clone_from(
        "https://github.com/django/django.git",
        DJANGO_SOURCE_DIRECTORY,
        progress=ProgressPrinter(),
        branch=branch,
        depth=100,
    )
    if commit_sha and repo.head.commit.hexsha != commit_sha:
        repo.remote("origin").fetch(branch, progress=ProgressPrinter(), depth=100)
        repo.git.checkout(commit_sha)
