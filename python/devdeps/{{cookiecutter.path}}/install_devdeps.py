#!/usr/bin/env python

import logging
import subprocess
import sys
from functools import partial

logging.basicConfig()
logger = logging.getLogger("devdeps")

run = partial(subprocess.run, check=True)

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


def main() -> int:
    try:
        _install_dependencies()
    except subprocess.CalledProcessError:
        return 1
    return 0


def _install_dependencies() -> None:
    package_manager = _get_package_manager()
    if package_manager == "poetry":
        run(["poetry", "add", "-D", *PACKAGES])
    else:
        run(["pip", "install", "--upgrade", "pip"])
        run(["pip", "install", "--upgrade", *PACKAGES])


def _get_package_manager() -> str:
    valid_choices = ["poetry", "pip"]
    default_choice = valid_choices[0]

    try:
        _, package_manager = sys.argv
    except ValueError:
        package_manager = default_choice

    if package_manager in valid_choices:
        return package_manager

    logger.warning(f"Invalid package manager: '{package_manager}'. Using poetry!")
    return default_choice


if __name__ == "__main__":
    raise SystemExit(main())
