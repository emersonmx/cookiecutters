import re
import subprocess
from functools import cache, partial
from pathlib import Path

run = partial(subprocess.run, check=True)


def main() -> int:
    initialize_git()
    update_pyproject_authors()
    update_devdeps()
    install_pre_commit()
    rename_gitignore()
    make_first_commit()
    return 0


def initialize_git() -> None:
    run(["git", "init"])


def update_pyproject_authors() -> None:
    author_name = get_author_name()
    author_email = get_author_email()
    pyproject_contents = get_pyproject_contents()
    line_found = pyproject_contents.index("authors = []\n")

    line = pyproject_contents[line_found]
    line = f'authors = ["{author_name} <{author_email}>"]\n'
    pyproject_contents[line_found] = line

    update_pyproject_contents(pyproject_contents)


@cache
def get_author_name() -> str:
    output = run(["git", "config", "user.name"], capture_output=True)
    return output.stdout.decode().strip()  # type: ignore


@cache
def get_author_email() -> str:
    output = run(["git", "config", "user.email"], capture_output=True)
    return output.stdout.decode().strip()  # type: ignore


@cache
def get_pyproject_contents() -> list[str]:
    file_path = get_pyproject_file_path()
    with open(file_path, "r") as f:
        return f.readlines()


def get_pyproject_file_path() -> str:
    return "pyproject.toml"


def update_pyproject_contents(contents: list[str]) -> None:
    file_path = get_pyproject_file_path()
    with open(file_path, "w") as f:
        f.writelines(contents)


def update_devdeps() -> None:
    devdeps = get_devdeps()
    run(["poetry", "add", "-D", *devdeps])


@cache
def get_devdeps() -> list[str]:
    pattern = re.compile("^(.*) = .*")
    pyproject_contents = get_pyproject_contents()
    start_line = (
        pyproject_contents.index("[tool.poetry.dev-dependencies]\n") + 1
    )
    end_line = start_line + pyproject_contents[start_line:].index("\n")
    text_range = pyproject_contents[start_line:end_line]

    return [pattern.sub("\\1@latest", line).strip() for line in text_range]


def install_pre_commit() -> None:
    run(["pre-commit", "install"])


def rename_gitignore() -> None:
    Path("_gitignore").rename(".gitignore")


def make_first_commit() -> None:
    run(["git", "add", "."])
    run(["git", "commit", "--no-verify", "-m", "Start project"])


if __name__ == "__main__":
    raise SystemExit(main())
