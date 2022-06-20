import json
import subprocess
from dataclasses import dataclass
from functools import cache, partial
from os import environ as env
from pathlib import Path
from typing import Any

import requests
from cookiecutter.main import cookiecutter  # type: ignore

run = partial(subprocess.run, check=True)


@dataclass
class Config:
    project_name: str
    project_slug: str
    git: bool  # TODO: Remove
    package_manager: str
    devdeps: bool  # TODO: Remove
    pre_commit: bool  # TODO: Remove


def main() -> int:
    config = _get_config()
    _show_python_info()

    if config.git:
        _setup_git()
        _create_readme()
        _create_gitignore()

    _setup_package_manager()

    if config.devdeps:
        _install_devdeps()

    _setup_templates()

    if config.pre_commit:
        _install_pre_commit()

    _cleanup()

    return 0


@cache
def _get_config() -> Config:
    with open("cookiecutter_configs.json") as f:
        config_data = json.load(f)

    project_name = config_data["project_name"]
    project_slug = _make_project_slug(project_name)
    git = config_data["git"] == "y"
    devdeps = config_data["devdeps"] == "y"
    pre_commit = all([git, devdeps])

    return Config(
        project_name=project_name,
        project_slug=project_slug,
        git=git,
        package_manager=config_data["package_manager"],
        devdeps=devdeps,
        pre_commit=pre_commit,
    )


def _make_project_slug(project_name: str) -> str:
    translations = str.maketrans({" ": "_", "-": "_"})
    return project_name.lower().translate(translations)


def _show_python_info() -> None:
    output = run(["python", "--version"], capture_output=True)
    print(f"Using {output.stdout.decode().strip()}")  # type: ignore # noqa


def _setup_git() -> None:
    run(["git", "init"])


def _create_readme() -> None:
    config = _get_config()
    project_name = config.project_name

    with open("README.md", "w") as f:
        f.write(f"# {project_name}\n")

    _git_add(["README.md"])
    _git_commit("Add README.md")


def _git_add(files: list[str]) -> None:
    run(["git", "add", *files])


def _git_commit(message: str) -> None:
    run(["git", "commit", "-m", message])


def _create_gitignore() -> None:
    response = requests.get("https://www.gitignore.io/api/python")
    response.raise_for_status()

    with open(".gitignore", "w") as f:
        f.write(response.text)

    _git_add([".gitignore"])
    _git_commit("Add gitignore")


def _setup_package_manager() -> None:
    config = _get_config()
    if config.package_manager == "poetry":
        _setup_poetry()
    else:
        _setup_pip()


def _setup_poetry() -> None:
    run(["poetry", "init", "-n"])
    run(["poetry", "install"])

    venv_dir = _get_poetry_venv_dir()
    venv_bin_dir = (Path(venv_dir) / "bin").absolute()
    env["PATH"] = f'{venv_bin_dir}:{env["PATH"]}'

    _git_add(["poetry.lock", "pyproject.toml"])
    _git_commit("Add poetry configs")


@cache
def _get_poetry_venv_dir() -> str:
    output = run(["poetry", "env", "info", "--path"], capture_output=True)
    return output.stdout.decode().strip()  # type: ignore


def _setup_pip() -> None:
    venv_dir = _get_venv_dir()
    run(["python", "-m", "venv", venv_dir])

    venv_bin_dir = (Path(venv_dir) / "bin").absolute()
    env["PATH"] = f'{venv_bin_dir}:{env["PATH"]}'
    run(["pip", "install", "--upgrade", "pip"])


def _get_venv_dir() -> str:
    return ".venv"


def _install_devdeps() -> None:
    _setup_template("python/devdeps")

    config = _get_config()
    if config.pre_commit:
        pre_commit_option = "--pre-commit"
    else:
        pre_commit_option = "--no-pre-commit"

    run(
        [
            "python",
            "./install_devdeps.py",
            "--package-manager",
            config.package_manager,
            pre_commit_option,
        ]
    )

    if config.package_manager == "poetry":
        _git_add(["poetry.lock", "pyproject.toml"])
        _git_commit("Install development dependencies")


def _setup_template(
    template: str,
    extra_context: dict[str, Any] | None = None,
) -> None:
    extra_context = extra_context or {}
    cookiecutters_url = "https://github.com/emersonmx/cookiecutters"
    current_dir = Path().absolute()

    print(f"Creating {template}...")  # noqa: T201
    cookiecutter(
        template=cookiecutters_url,
        no_input=True,
        overwrite_if_exists=True,
        directory=template,
        extra_context={
            "path": current_dir,
            **extra_context,
        },
    )


def _setup_templates() -> None:
    config = _get_config()

    if config.pre_commit:
        _create_pre_commit_template()

    _create_editorconfig_template()
    _create_direnv_template()

    if config.devdeps:
        _create_isort_template()
        _create_black_template()
        _create_flake8_template()
        _create_mypy_template()
        _create_vulture_template()
        _create_invoke_run_template()
        _create_invoke_format_template()
        _create_invoke_lint_template()
        _create_invoke_tests_template()

    _create_hello_world_template()
    _create_tests_template()


def _create_pre_commit_template() -> None:
    _setup_template("python/pre-commit")
    _git_add([".pre-commit-config.yaml"])
    _git_commit("Add pre-commit config")


def _create_editorconfig_template() -> None:
    _setup_template("python/editorconfig")
    _git_add([".editorconfig"])
    _git_commit("Add editorconfig")


def _create_direnv_template() -> None:
    _setup_template("python/direnv", {})  # TODO: Add venv_path

    run(
        ["ex", "-", ".envrc"],
        input=b"$\nd\n%\nw\n",
    )
    run(
        ["ex", "-", ".gitignore"],
        input=b"/^# Environments\n/^$\ni\n.envrc\n.\nw\n",
    )

    _git_add([".gitignore"])
    _git_commit("Ignore .envrc")


def _create_isort_template() -> None:
    _setup_template("python/isort")
    _git_add(["pyproject.toml"])
    _git_commit("Add isort configs")


def _create_black_template() -> None:
    _setup_template("python/black")
    _git_add(["pyproject.toml"])
    _git_commit("Add black configs")


def _create_flake8_template() -> None:
    _setup_template("python/flake8")
    _git_add([".flake8"])
    _git_commit("Add flake8 configs")


def _create_mypy_template() -> None:
    _setup_template("python/mypy")
    _git_add(["pyproject.toml"])
    _git_commit("Add mypy configs")


def _create_vulture_template() -> None:
    _setup_template("python/vulture")
    _git_add(["pyproject.toml"])
    _git_commit("Add vulture configs")


def _create_invoke_run_template() -> None:
    _setup_template("python/invoke/run")
    _git_add(["tasks.py"])
    _git_commit("Add run task")


def _create_invoke_format_template() -> None:
    config = _get_config()
    pre_commit = "y" if config.pre_commit else "n"
    _setup_template("python/invoke/format", {"use_pre_commit": pre_commit})

    _git_add(["tasks.py"])
    _git_commit("Add format task")


def _create_invoke_lint_template() -> None:
    config = _get_config()
    pre_commit = "y" if config.pre_commit else "n"
    _setup_template("python/invoke/lint", {"use_pre_commit": pre_commit})

    _git_add(["tasks.py"])
    _git_commit("Add lint task")


def _create_invoke_tests_template() -> None:
    _setup_template("python/invoke/tests")
    _git_add(["tasks.py"])
    _git_commit("Add tests task")


def _create_hello_world_template() -> None:
    _setup_template("python/hello_world")
    _git_add(["main.py"])
    _git_commit("Add main.py")


def _create_tests_template() -> None:
    _setup_template("python/tests")
    _git_add(["pyproject.toml", "tests/"])
    _git_commit("Add tests")


def _install_pre_commit() -> None:
    run(["pre-commit", "install"])


def _cleanup() -> None:
    Path("install_devdeps.py").unlink(missing_ok=True)
    Path("cookiecutter_configs.json").unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
