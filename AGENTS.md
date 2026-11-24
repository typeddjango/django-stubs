# django-stubs

**Gate**: `just pre-mr-check` must be green before every push. Master is green, so every failure, local or CI, is yours:
fix it and rerun until green; on unexpected results, `just clean-cache` first.
A missing system library (GDAL, GEOS, MySQL client) is your user's to install, see CONTRIBUTING.md.

CONTRIBUTING.md also covers model-based tests, private attributes and stubtest allowlists.

## Typing

- **Stubs-first**: fix typing in `django-stubs/**/*.pyi` so mypy, pyright, pyrefly and ty all benefit;
  add `mypy_django_plugin/` code only to bridge a gap mypy alone can't handle yet.
  Don't remove an existing plugin hook if the error message gets vaguer
  or the stubs must copy an external API by hand (e.g. `str` methods on `_StrPromise`).
- **Source-backed**: read the Django source (installed under `.venv`) for every type you write,
  and link a GitHub permalink to it in the PR for anything non-trivial.
- **Reuse**: search the repo for an existing helper, alias or naming pattern first, and follow it.
- **Precise**: fix an error by getting the type right. `Any` or an ignore is right only when it mirrors Django
  (an override that breaks LSP, an argument Django accepts as anything) or works around a type-checker bug.
- **Link the issue**: every type-checker bug workaround (odd signature, extra overload, per-checker ignore)
  carries a comment linking the upstream issue.
- **Comments say why, in a line**: a comment that needs a paragraph is covering a bad fix; fix the code.

## Tests

- New tests are `assert_type` tests under `tests/assert_type/`, with per-checker ignores
  when only the mypy plugin supports the behavior; yml only for what they can't express, such as plugin error messages.
- Write tests the way a Django project uses the API, from the issue's snippet when it has one.

## Pull requests

- **Human in the loop**: your user writes issue comments and review replies in their own words;
  hand them the facts. Policy: `.github/AI_POLICY.md`.
- **Description**: keep `.github/pull_request_template.md` whole and fill it with what the diff can't show:
  what was wrong and why the fix is right, in five sentences at most, plus a code snippet when it explains better.
  The AI Policy box is your user's to tick.
- Commits and PR descriptions carry no coding-agent attribution (`Co-Authored-By`, "Generated with").
