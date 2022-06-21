import json
import subprocess
from dataclasses import dataclass
from functools import cache, partial
from os import environ as env
from pathlib import Path
from typing import Any

import requests
from cookiecutter.config import get_user_config as get_cookiecutter_config
from cookiecutter.main import cookiecutter

run = partial(subprocess.run, check=True)


@dataclass
class Config:
    project_name: str
    project_slug: str
    package_manager: str


def main() -> int:
    _show_python_version()

    _initialize_git()
    _add_readme()
    _add_gitignore()

    _create_virtualenv()

    _install_devdeps()

    _add_editorconfig()
    _create_envrc()
    _ignore_envrc()
    _create_an_empty_module()
    _add_isort_config()
    _add_black_config()
    _add_flake8_config()
    _add_mypy_config()
    _add_vulture_config()
    _add_run_task()
    _add_format_task()
    _add_lint_task()
    _add_tests_task()
    _create_tests_directory()

    _install_pre_commit()

    _cleanup()

    return 0


def _show_python_version() -> None:
    output = run(["python", "--version"], capture_output=True)
    print(f"Using {output.stdout.decode().strip()}")  # type: ignore # noqa


def _initialize_git() -> None:
    run(["git", "init"])


def _add_readme() -> None:
    config = _get_config()
    project_name = config.project_name

    with open("README.md", "w") as f:
        f.write(f"# {project_name}\n")

    _git_add(["README.md"])
    _git_commit("Add README")


@cache
def _get_config() -> Config:
    with open("cookiecutter_configs.json") as f:
        config_data = json.load(f)

    project_name = config_data["project_name"]
    project_slug = _make_project_slug(project_name)

    return Config(
        project_name=project_name,
        project_slug=project_slug,
        package_manager=config_data["package_manager"],
    )


def _make_project_slug(project_name: str) -> str:
    translations = str.maketrans({" ": "_", "-": "_"})
    return project_name.lower().translate(translations)


def _git_add(files: list[str]) -> None:
    run(["git", "add", *files])


def _git_commit(message: str) -> None:
    run(["git", "commit", "-m", message])


def _add_gitignore() -> None:
    response = requests.get("https://www.gitignore.io/api/python")
    response.raise_for_status()

    with open(".gitignore", "w") as f:
        f.write(response.text)

    _git_add([".gitignore"])
    _git_commit("Add gitignore")


def _create_virtualenv() -> None:
    config = _get_config()
    if config.package_manager == "poetry":
        _create_virtualenv_with_poetry()
    else:
        _create_virtualenv_with_venv()


def _create_virtualenv_with_poetry() -> None:
    run(["poetry", "init", "-n"])
    run(["poetry", "install"])

    venv_dir = _get_poetry_venv_dir()
    venv_bin_dir = (Path(venv_dir) / "bin").absolute()
    env["PATH"] = f'{venv_bin_dir}:{env["PATH"]}'

    _git_add(["poetry.lock", "pyproject.toml"])
    _git_commit("Initialize poetry")


@cache
def _get_poetry_venv_dir() -> str:
    output = run(["poetry", "env", "info", "--path"], capture_output=True)
    venv_dir: str = output.stdout.decode().strip()  # type: ignore
    default_dir = _get_default_venv_dir()
    current_dir = Path().absolute()
    if str(current_dir / default_dir) == venv_dir:
        return default_dir
    return venv_dir


def _get_default_venv_dir() -> str:
    return ".venv"


def _create_virtualenv_with_venv() -> None:
    venv_dir = _get_default_venv_dir()
    run(["python", "-m", "venv", venv_dir])

    venv_bin_dir = (Path(venv_dir) / "bin").absolute()
    env["PATH"] = f'{venv_bin_dir}:{env["PATH"]}'
    run(["pip", "install", "--upgrade", "pip"])


def _get_cookiecutters_dir() -> str:
    config = get_cookiecutter_config()
    cookiecutter_dir = Path(config["cookiecutters_dir"]) / "cookiecutters"
    return str(cookiecutter_dir.absolute())


def _install_devdeps() -> None:
    _create_from_template("python/devdeps")

    config = _get_config()

    run(
        [
            "python",
            "./install_devdeps.py",
            "--package-manager",
            config.package_manager,
            "--pre-commit",
        ]
    )

    if config.package_manager == "poetry":
        _git_add(["poetry.lock", "pyproject.toml"])
        _git_commit("Install development dependencies")


def _create_from_template(
    template: str,
    extra_context: dict[str, Any] | None = None,
) -> None:
    extra_context = extra_context or {}
    current_dir = Path().absolute()

    print(f"Creating {template}...")  # noqa: T201
    cookiecutter(
        template=_get_cookiecutters_dir(),
        no_input=True,
        overwrite_if_exists=True,
        directory=template,
        extra_context={
            "path": current_dir,
            **extra_context,
        },
    )


def _add_editorconfig() -> None:
    _create_from_template("python/editorconfig")
    _git_add([".editorconfig"])
    _git_commit("Add editorconfig")


def _create_envrc() -> None:
    config = _get_config()
    venv_path = _get_default_venv_dir()
    if config.package_manager == "poetry":
        venv_path = _get_poetry_venv_dir()

    _create_from_template("python/direnv", {"venv_path": venv_path})


def _ignore_envrc() -> None:
    _ex(".envrc", "g/^#/d\n$\nd\nw\n")
    _ex(".gitignore", "/^# Environments\n/^$\ni\n.envrc\n.\nw\n")

    _git_add([".gitignore"])
    _git_commit("Ignore .envrc")


def _ex(filepath: str, script: str) -> None:
    run(["ex", "-", filepath], input=script.encode())


def _create_an_empty_module() -> None:
    config = _get_config()
    module_name = f"{config.project_slug}.py"
    module_path = Path(module_name)
    module_path.touch(exist_ok=True)

    _git_add([module_name])
    _git_commit(f"Add {module_name}")


def _add_isort_config() -> None:
    _create_from_template("python/isort")
    _git_add(["pyproject.toml"])
    _git_commit("Add isort config")


def _add_black_config() -> None:
    _create_from_template("python/black")
    _git_add(["pyproject.toml"])
    _git_commit("Add black config")


def _add_flake8_config() -> None:
    _create_from_template("python/flake8")
    _git_add([".flake8"])
    _git_commit("Add flake8 config")


def _add_mypy_config() -> None:
    _create_from_template("python/mypy")
    _git_add(["pyproject.toml"])
    _git_commit("Add mypy config")


def _add_vulture_config() -> None:
    _create_from_template("python/vulture")
    _git_add(["pyproject.toml"])
    _git_commit("Add vulture config")


def _add_run_task() -> None:
    config = _get_config()
    project_slug = config.project_slug
    _create_from_template(
        "python/invoke/run",
        {"command": f"python {project_slug}.py"},
    )
    _git_add(["tasks.py"])
    _git_commit("Add run task")


def _add_format_task() -> None:
    _create_from_template("python/invoke/format", {"use_pre_commit": "y"})
    _git_add(["tasks.py"])
    _git_commit("Add format task")


def _add_lint_task() -> None:
    _create_from_template("python/invoke/lint", {"use_pre_commit": "y"})
    _git_add(["tasks.py"])
    _git_commit("Add lint task")


def _add_tests_task() -> None:
    _create_from_template("python/invoke/tests")
    _git_add(["tasks.py"])
    _git_commit("Add tests task")


def _create_tests_directory() -> None:
    tests_path = Path("tests").absolute()
    tests_path.mkdir(parents=True, exist_ok=True)
    (tests_path / "__init__.py").touch(exist_ok=True)

    _git_add(["tests/__init__.py"])
    _git_commit("Add tests directory")


def _install_pre_commit() -> None:
    _create_from_template("python/pre-commit")

    _exclude_tests_dir_in_bandit()

    if Path(_get_default_venv_dir()).exists():
        _exclude_venv_dir_in_vulture()

    _git_add([".pre-commit-config.yaml", "pyproject.toml"])
    _git_commit("Add pre-commit config")

    run(["pre-commit", "install"])


def _exclude_tests_dir_in_bandit() -> None:
    exclude_tests = "\n".join(
        [
            "/id: bandit",
            "a",
            "        exclude: |",
            "          (?x)(",
            "            tests/",
            "          )",
            ".",
            "w",
            "",
        ]
    )
    _ex(".pre-commit-config.yaml", exclude_tests)


def _exclude_venv_dir_in_vulture() -> None:
    _ex(
        "pyproject.toml",
        '/tool.vulture\n/paths\na\nexclude = [".venv/"]\n.\nw\n',
    )


def _cleanup() -> None:
    Path("install_devdeps.py").unlink(missing_ok=True)
    Path("cookiecutter_configs.json").unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
