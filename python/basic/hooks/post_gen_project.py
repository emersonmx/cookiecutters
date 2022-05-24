import os
from subprocess import DEVNULL, CalledProcessError, run

import requests

PACKAGES = [
    # formatting
    "add-trailing-comma",
    "black",
    "isort",
    # linting
    "types-all",
    "flake8",
    "flake8-print",
    "pep8-naming",
    "mypy",
    "vulture",
    "bandit",
    # testing
    "pytest",
    "hypothesis",
    "coverage",
    # debug
    "ipdb",
    # make
    "invoke",
    # misc
    "pre-commit",
]


def _setup_poetry() -> None:
    run(["poetry", "init", "-n", "--python", "^3.10"])
    run(["poetry", "add", "-D", *PACKAGES])
    _setup_pyproject()


def _setup_pyproject() -> None:
    with open("tools_pyproject.toml") as f:
        tools_pyproject_data = f.read()
    with open("pyproject.toml", "a+") as f:
        if tools_pyproject_data:
            f.write(tools_pyproject_data)
    os.remove("tools_pyproject.toml")


def _setup_pre_commit() -> None:
    run(["git", "init"])
    run(["poetry", "run", "pre-commit", "install"])
    run(["poetry", "run", "pre-commit", "autoupdate"], stdout=DEVNULL)


def _setup_gitignore() -> None:
    gitignore_url = "https://www.toptal.com/developers/gitignore/api/python"
    response = requests.get(gitignore_url)
    response.raise_for_status()
    data = response.text
    with open(".gitignore", "w+") as f:
        f.write(data)


def setup_project() -> None:
    _setup_poetry()
    _setup_pre_commit()


def commit_files() -> None:
    _setup_gitignore()
    run(["git", "add", "."])
    run(["git", "commit", "-m", "Start project"])


def main() -> int:
    try:
        setup_project()
        commit_files()
    except CalledProcessError:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
