import json
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from subprocess import run

import requests
from cookiecutter.main import cookiecutter  # type: ignore


@dataclass
class Config:
    project_name: str
    project_slug: str
    setup_git: bool
    setup_gitignore: bool
    package_manager: str
    install_devdeps: bool
    install_pre_commit: bool


def main() -> int:
    config = _get_config()
    _show_python_info()

    if config.setup_git:
        _setup_git()
        if config.setup_gitignore:
            _setup_gitignore()

    if config.package_manager == "poetry":
        _setup_poetry()
    else:
        _setup_pip()

    if config.install_devdeps:
        _install_devdeps()

    _setup_templates()

    if _is_pre_commit_enabled():
        _install_pre_commit()

    _cleanup()

    return 0


@cache
def _get_config() -> Config:
    with open("cookiecutter_configs.json") as f:
        config_data = json.load(f)
    return Config(**config_data)


def _show_python_info() -> None:
    run(["python", "--version"])


def _setup_git() -> None:
    config = _get_config()
    project_name = config.project_name

    run(["git", "init"])

    with open("README.md", "w") as f:
        f.write(f"# {project_name}")

    run(["git", "add", "README.md"])
    run(["git", "commit", "-m", "'Start project'"])


def _setup_gitignore() -> None:
    response = requests.get("https://www.gitignore.io/api/python")
    response.raise_for_status()

    with open(".gitignore", "w") as f:
        f.write(response.text)

    run(["git", "add", ".gitignore"])
    run(["git", "commit", "-m", "'Add gitignore'"])


def _setup_poetry() -> None:
    run(["poetry", "init", "-n"])
    run(["poetry", "install"])


def _setup_pip() -> None:
    run(["python", "-m", "venv", _get_venv_dir()])
    venv_python_bin = _get_venv_python_bin()
    run([venv_python_bin, "-m", "pip", "install", "--upgrade", "pip"])


def _get_venv_dir() -> str:
    return ".venv"


def _get_venv_python_bin() -> str:
    venv_bin_dir = _get_venv_bin_dir()
    return str(Path(f"{venv_bin_dir}/python").absolute())


def _get_venv_bin_dir() -> str:
    venv_dir = _get_venv_dir()
    return str(Path(f"{venv_dir}/bin").absolute())


def _install_devdeps() -> None:
    config = _get_config()
    package_manager = config.package_manager

    _setup_template("python/devdeps")

    if config.package_manager == "poetry":
        run(["poetry", "run", "./install_devdeps.py", package_manager])
    else:
        python_bin = _get_venv_python_bin()
        run([python_bin, "./install_devdeps.py", package_manager])


def _setup_template(template: str, extra_context: dict | None = None) -> None:
    extra_context = extra_context or {}
    cookiecutters_url = "https://github.com/emersonmx/cookiecutters"
    current_dir = Path().absolute()
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
    use_pre_commit = _is_pre_commit_enabled()

    use_pre_commit_input = "y" if use_pre_commit else "n"
    templates: dict[str, dict] = {
        "python/pre-commit": {},
        "python/editorconfig": {},
        "python/direnv": {},
        "python/isort": {},
        "python/black": {},
        "python/flake8": {},
        "python/mypy": {},
        "python/vulture": {},
        "python/invoke/run": {},
        "python/invoke/format": {"use_pre_commit": use_pre_commit_input},
        "python/invoke/lint": {"use_pre_commit": use_pre_commit_input},
        "python/invoke/tests": {},
        "python/hello_world": {},
        "python/tests": {},
    }
    for template, context in templates.items():
        _setup_template(template, context)


def _is_pre_commit_enabled() -> bool:
    config = _get_config()
    return all(
        [
            config.setup_git,
            config.install_pre_commit,
        ]
    )


def _install_pre_commit() -> None:
    config = _get_config()
    if config.package_manager == "poetry":
        run(["poetry", "run", "pre-commit", "install"])
    else:
        venv_bin_dir = Path(_get_venv_bin_dir())
        precommit_bin = str((venv_bin_dir / "pre-commit").absolute())
        run([precommit_bin, "install"])


def _cleanup() -> None:
    Path("install_devdeps.py").unlink(missing_ok=True)
    Path("cookiecutter_configs.json").unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
