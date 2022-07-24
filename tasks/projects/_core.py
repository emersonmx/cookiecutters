import tempfile
from functools import cache
from pathlib import Path

from tasks.utils import create_from_template, get_root_directory


def remove_devdeps() -> None:
    contents = get_pyproject_contents()
    start_line = contents.index("[tool.poetry.dev-dependencies]\n") + 1
    end_line = start_line + contents[start_line:].index("\n")
    del contents[start_line:end_line]
    update_pyproject_contents(contents)


@cache
def get_pyproject_contents() -> list[str]:
    file_path = get_pyproject_file_path()
    with open(file_path) as f:
        return f.readlines()


def get_pyproject_file_path() -> str:
    return str(get_project_template_path() / "pyproject.toml")


def get_project_template_path() -> Path:
    return (
        get_root_directory()
        / "projects"
        / "python"
        / "{{cookiecutter.project_name}}"
    )


def update_pyproject_contents(contents: list[str]) -> None:
    file_path = get_pyproject_file_path()
    with open(file_path, "w") as f:
        f.writelines(contents)


def update_devdeps() -> None:
    deps = [f'{dep} = ""\n' for dep in get_devdeps()]
    contents = get_pyproject_contents()
    line_index = contents.index("[tool.poetry.dev-dependencies]\n") + 1
    contents = contents[:line_index] + deps + contents[line_index:]
    update_pyproject_contents(contents)


@cache
def get_devdeps() -> list[str]:
    with tempfile.TemporaryDirectory() as tmp_dir:
        create_from_template("python/devdeps", {"path": tmp_dir})
        tmp_dir_path = str(Path(tmp_dir) / "requirements-dev.txt")
        with open(tmp_dir_path) as f:
            return [line.strip() for line in f.readlines()]
