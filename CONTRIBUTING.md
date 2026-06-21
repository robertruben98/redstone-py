# Contributing to redstone-py

Thanks for your interest in improving redstone-py! This project follows
test-driven development — please add a failing test before the code that makes it pass.

## Setup

```bash
git clone https://github.com/robertruben98/redstone-py
cd redstone-py
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Quality gates

All of these must pass before a PR is merged (CI enforces them on Python 3.9–3.13):

```bash
ruff check .            # lint
ruff format --check .   # formatting
mypy --strict src tests # types
pytest                  # unit tests (live integration test is deselected)
```

The live integration test hits the real, keyless RedStone API. Run it explicitly:

```bash
pytest -m integration
```

## Workflow

1. Create a branch off `main` (e.g. `feat/...`, `fix/...`).
2. Write a failing test, then the minimal code to pass it.
3. Keep the suite, types, and lint green.
4. Update `CHANGELOG.md` under `[Unreleased]`.
5. Open a PR. Releases are published to PyPI via OIDC Trusted Publishing when a
   `v*` tag is pushed.

## Code style

- Target Python 3.9+: use builtin generics (`list[...]`, `dict[...]`) but keep
  `typing.Optional`/`typing.Union` rather than PEP 604 `X | None` in runtime
  (pydantic) annotations, since that syntax is not valid at runtime on 3.9.
- Public methods carry Google-style docstrings; model fields carry
  `Field(description=...)`.
