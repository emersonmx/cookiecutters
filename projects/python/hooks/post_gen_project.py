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
    git: bool
    package_manager: str
    devdeps: bool
    pre_commit: bool


def main() -> int:
    config = _get_config()
    _show_python_info()

    if config.git:
        _setup_git()
        _setup_gitignore()

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
    config = _get_config()
    project_name = config.project_name

    run(["git", "init"])

    with open("README.md", "w") as f:
        f.write(f"# {project_name}\n")

    run(["git", "add", "README.md"])
    run(["git", "commit", "-m", "Start project"])


def _setup_gitignore() -> None:
    response = requests.get("https://www.gitignore.io/api/python")
    response.raise_for_status()

    with open(".gitignore", "w") as f:
        f.write(response.text)

    run(["git", "add", ".gitignore"])
    run(["git", "commit", "-m", "Add gitignore"])


def _setup_package_manager() -> None:
    config = _get_config()
    if config.package_manager == "poetry":
        _setup_poetry()
    else:
        _setup_pip()


def _setup_poetry() -> None:
    run(["poetry", "init", "-n"])
    run(["poetry", "install"])

    output = run(["poetry", "env", "info", "--path"], capture_output=True)
    venv_dir = output.stdout.decode().strip()  # type: ignore
    venv_bin_dir = (Path(venv_dir) / "bin").absolute()
    env["PATH"] = f'{venv_bin_dir}:{env["PATH"]}'


def _setup_pip() -> None:
    venv_dir = ".venv"
    run(["python", "-m", "venv", venv_dir])

    venv_bin_dir = (Path(venv_dir) / "bin").absolute()
    env["PATH"] = f'{venv_bin_dir}:{env["PATH"]}'
    run(["pip", "install", "--upgrade", "pip"])


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
    for template, context in _get_templates().items():
        _setup_template(template, context)


def _get_templates() -> dict[str, Any]:
    config = _get_config()
    pre_commit = config.pre_commit
    pre_commit_input = "y" if pre_commit else "n"

    templates = {
        "python/pre-commit": {},
        "python/editorconfig": {},
        "python/direnv": {},
        "python/isort": {},
        "python/black": {},
        "python/flake8": {},
        "python/mypy": {},
        "python/vulture": {},
        "python/invoke/run": {},
        "python/invoke/format": {"use_pre_commit": pre_commit_input},
        "python/invoke/lint": {"use_pre_commit": pre_commit_input},
        "python/invoke/tests": {},
        "python/hello_world": {},
        "python/tests": {},
    }

    templates_to_remove = []
    if not pre_commit:
        templates_to_remove.append("python/pre-commit")
    if not config.devdeps:
        templates_to_remove.extend(
            [
                "python/isort",
                "python/black",
                "python/flake8",
                "python/mypy",
                "python/vulture",
                "python/invoke/run",
                "python/invoke/format",
                "python/invoke/lint",
                "python/invoke/tests",
                "python/tests",
            ]
        )

    for template in templates_to_remove:
        templates.pop(template, None)

    return templates


def _install_pre_commit() -> None:
    run(["pre-commit", "install"])


def _cleanup() -> None:
    Path("install_devdeps.py").unlink(missing_ok=True)
    Path("cookiecutter_configs.json").unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
