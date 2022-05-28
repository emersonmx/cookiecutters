#!/usr/bin/env python

import sys
from subprocess import CalledProcessError, run

PACKAGES = [
    # tools
    "pytest",
    "hypothesis",
    "coverage",
    "ipdb",
    "invoke",
    "pre-commit",
    # code quality
    "pyupgrade",
    "add-trailing-comma",
    "yesqa",
    "isort",
    "black",
    "flake8",
    "flake8-print",
    "pep8-naming",
    "mypy",
    "vulture",
    "bandit",
    # stubs
    "types-all",
]


def _install_dependencies() -> None:
    {%- if cookiecutter.package_manager == "poetry" %}
    run(["poetry", "add", "-D", *PACKAGES])
    {%- else %}
    run(["pip", "install", "--upgrade", "pip"])
    run(["pip", "install", "--upgrade", *PACKAGES])
    {%- endif %}


def _remove_script() -> None:
    run(["rm", "-f", sys.argv[0]])


def main() -> int:
    try:
        _install_dependencies()
        _remove_script()
    except CalledProcessError:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
