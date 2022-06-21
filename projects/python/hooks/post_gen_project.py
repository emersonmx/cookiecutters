import json
import subprocess
from functools import cache, partial
from os import environ as env
from pathlib import Path
from typing import Any

import requests
from cookiecutter.config import get_user_config as get_cookiecutter_config
from cookiecutter.main import cookiecutter

run = partial(subprocess.run, check=True)


def main() -> int:
    show_python_version()

    initialize_git()
    add_readme()
    add_gitignore()

    create_virtualenv()

    install_devdeps()

    add_editorconfig()
    create_envrc()
    ignore_envrc()
    create_an_empty_module()
    add_isort_config()
    add_black_config()
    add_flake8_config()
    add_mypy_config()
    add_vulture_config()
    add_run_task()
    add_format_task()
    add_lint_task()
    add_tests_task()
    create_tests_directory()

    install_pre_commit()

    cleanup()

    return 0


def show_python_version() -> None:
    python_version = get_python_version()
    print(f"Using {python_version}")  # noqa: T201


def get_python_version() -> str:
    output = run(["python", "--version"], capture_output=True)
    return output.stdout.decode().strip()  # type: ignore # noqa


def initialize_git() -> None:
    run(["git", "init"])


def add_readme() -> None:
    create_readme()
    git_add(["README.md"])
    git_commit("Add README")


def create_readme() -> None:
    project_name = get_project_name()
    with open("README.md", "w") as f:
        f.write(f"# {project_name}\n")


def get_project_name() -> str:
    config = get_config()
    return config["project_name"]


@cache
def get_config() -> dict:
    config_data = load_config_json()
    project_name = config_data["project_name"]
    project_slug = make_project_slug(project_name)
    return {
        "project_name": project_name,
        "project_slug": project_slug,
        "package_manager": config_data["package_manager"],
    }


def load_config_json() -> dict:
    with open("cookiecutter_configs.json") as f:
        return json.load(f)


def make_project_slug(project_name: str) -> str:
    translations = str.maketrans({" ": "_", "-": "_"})
    return project_name.lower().translate(translations)


def git_add(files: list[str]) -> None:
    run(["git", "add", *files])


def git_commit(message: str) -> None:
    run(["git", "commit", "-m", message])


def add_gitignore() -> None:
    create_gitignore()
    git_add([".gitignore"])
    git_commit("Add gitignore")


def create_gitignore() -> None:
    gitignore_data = get_gitignore_data()
    with open(".gitignore", "w") as f:
        f.write(gitignore_data)


def get_gitignore_data() -> str:
    response = requests.get("https://www.gitignore.io/api/python")
    response.raise_for_status()
    return response.text


def create_virtualenv() -> None:
    if is_using_poetry():
        create_virtualenv_with_poetry()
    else:
        create_virtualenv_with_venv()


def is_using_poetry() -> bool:
    return get_package_manager() == "poetry"


def get_package_manager() -> str:
    config = get_config()
    return config["package_manager"]


def create_virtualenv_with_poetry() -> None:
    run(["poetry", "init", "-n"])
    run(["poetry", "install"])

    venv_bin_dir = get_poetry_virtualenv_bin_directory()
    add_directory_to_environment_path(venv_bin_dir)

    git_add(["poetry.lock", "pyproject.toml"])
    git_commit("Initialize poetry")


def get_poetry_virtualenv_bin_directory() -> str:
    venv_dir = get_poetry_virtualenv_directory()
    return str((Path(venv_dir) / "bin").absolute())


@cache
def get_poetry_virtualenv_directory() -> str:
    output = run(["poetry", "env", "info", "--path"], capture_output=True)
    venv_dir: str = output.stdout.decode().strip()  # type: ignore
    if is_pointing_to_local_venv(venv_dir):
        return get_virtualenv_directory()
    return venv_dir


def is_pointing_to_local_venv(virtualenv_dir: str) -> bool:
    default_venv_dir = get_virtualenv_directory()
    current_dir = Path().absolute()
    return str(current_dir / default_venv_dir) == virtualenv_dir


def get_virtualenv_directory() -> str:
    return ".venv"


def add_directory_to_environment_path(directory: str) -> None:
    env["PATH"] = f'{directory}:{env["PATH"]}'


def create_virtualenv_with_venv() -> None:
    run(["python", "-m", "venv", get_virtualenv_directory()])
    add_directory_to_environment_path(get_venv_bin_directory())
    run(["pip", "install", "--upgrade", "pip"])


def get_venv_bin_directory() -> str:
    venv_dir = get_virtualenv_directory()
    return str((Path(venv_dir) / "bin").absolute())


def install_devdeps() -> None:
    create_from_template("python/devdeps")

    run(
        [
            "python",
            "./install_devdeps.py",
            "--package-manager",
            get_package_manager(),
            "--pre-commit",
        ]
    )

    if is_using_poetry():
        git_add(["poetry.lock", "pyproject.toml"])
        git_commit("Install development dependencies")


def create_from_template(
    template: str,
    extra_context: dict[str, Any] | None = None,
) -> None:
    extra_context = extra_context or {}
    current_dir = Path().absolute()

    print(f"Creating {template}...")  # noqa: T201
    cookiecutter(
        template=get_cookiecutters_dir(),
        no_input=True,
        overwrite_if_exists=True,
        directory=template,
        extra_context={
            "path": current_dir,
            **extra_context,
        },
    )


def get_cookiecutters_dir() -> str:
    config = get_cookiecutter_config()
    cookiecutter_dir = Path(config["cookiecutters_dir"]) / "cookiecutters"
    return str(cookiecutter_dir.absolute())


def add_editorconfig() -> None:
    create_from_template("python/editorconfig")
    git_add([".editorconfig"])
    git_commit("Add editorconfig")


def create_envrc() -> None:
    venv_path = get_virtualenv_directory()
    if is_using_poetry():
        venv_path = get_poetry_virtualenv_directory()

    create_from_template("python/direnv", {"venv_path": venv_path})


def ignore_envrc() -> None:
    run_ex(".gitignore", "/^# Environments\n/^$\ni\n.envrc\n.\nw\n")
    git_add([".gitignore"])
    git_commit("Ignore .envrc")


def run_ex(filepath: str, script: str) -> None:
    run(["ex", "-", filepath], input=script.encode())


def create_an_empty_module() -> None:
    project_slug = get_project_slug()
    module_name = f"{project_slug}.py"
    module_path = Path(module_name)
    module_path.touch(exist_ok=True)

    git_add([module_name])
    git_commit(f"Add {module_name}")


def get_project_slug() -> str:
    config = get_config()
    return config["project_slug"]


def add_isort_config() -> None:
    create_from_template("python/isort")
    git_add(["pyproject.toml"])
    git_commit("Add isort config")


def add_black_config() -> None:
    create_from_template("python/black")
    git_add(["pyproject.toml"])
    git_commit("Add black config")


def add_flake8_config() -> None:
    create_from_template("python/flake8")
    git_add([".flake8"])
    git_commit("Add flake8 config")


def add_mypy_config() -> None:
    create_from_template("python/mypy")
    git_add(["pyproject.toml"])
    git_commit("Add mypy config")


def add_vulture_config() -> None:
    exclude_paths = []
    if is_virtualenv_directory_exists():
        exclude_paths.append(get_virtualenv_directory())

    create_from_template(
        "python/vulture",
        {
            "exclude_paths": json.dumps(exclude_paths),
        },
    )

    git_add(["pyproject.toml"])
    git_commit("Add vulture config")


def is_virtualenv_directory_exists() -> bool:
    return Path(get_virtualenv_directory()).exists()


def add_run_task() -> None:
    project_slug = get_project_slug()
    create_from_template(
        "python/invoke/run",
        {"command": f"python {project_slug}.py"},
    )
    git_add(["tasks.py"])
    git_commit("Add run task")


def add_format_task() -> None:
    create_from_template("python/invoke/format", {"use_pre_commit": "y"})
    git_add(["tasks.py"])
    git_commit("Add format task")


def add_lint_task() -> None:
    create_from_template("python/invoke/lint", {"use_pre_commit": "y"})
    git_add(["tasks.py"])
    git_commit("Add lint task")


def add_tests_task() -> None:
    create_from_template("python/invoke/tests")
    git_add(["tasks.py"])
    git_commit("Add tests task")


def create_tests_directory() -> None:
    tests_path = Path("tests").absolute()
    tests_path.mkdir(parents=True, exist_ok=True)
    (tests_path / "__init__.py").touch(exist_ok=True)

    git_add(["tests/__init__.py"])
    git_commit("Add tests directory")


def install_pre_commit() -> None:
    create_from_template("python/pre-commit")

    git_add([".pre-commit-config.yaml", "pyproject.toml"])
    git_commit("Add pre-commit config")

    run(["pre-commit", "install"])


def cleanup() -> None:
    Path("install_devdeps.py").unlink(missing_ok=True)
    Path("cookiecutter_configs.json").unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
