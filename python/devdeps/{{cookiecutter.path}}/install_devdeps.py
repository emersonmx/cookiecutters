#!/usr/bin/env python

import argparse
import logging
import subprocess
from functools import cache, partial

logging.basicConfig()
logger = logging.getLogger("devdeps")

run = partial(subprocess.run, check=True)


def main() -> int:
    try:
        _install_dependencies()
    except subprocess.CalledProcessError:
        return 1
    return 0


def _install_dependencies() -> None:
    args = _get_args()
    if args.package_manager == "poetry":
        _install_with_poetry()
    else:
        _install_with_pip()


def _install_with_poetry() -> None:
    packages = _get_packages()
    run(["poetry", "add", "-D", *packages])


def _get_packages() -> list:
    args = _get_args()
    return [
        # tools
        "pytest",
        "hypothesis",
        "coverage",
        "ipdb",
        "invoke",
        *(["pre-commit"] if args.pre_commit else []),
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


def _install_with_pip() -> None:
    packages = _get_packages()
    run(["pip", "install", "--upgrade", *packages])


@cache
def _get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--package-manager",
        choices=["poetry", "pip"],
        default="poetry",
    )
    parser.add_argument(
        "--pre-commit",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    return parser.parse_args()


if __name__ == "__main__":
    raise SystemExit(main())
