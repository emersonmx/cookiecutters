import os
import shutil


class Poetry:
    def __init__(self) -> None:
        self.binary_name = "poetry"
        if not shutil.which(self.binary_name):
            raise RuntimeError("Poetry not found")

    def init(self, python_version: str) -> None:
        os.system(f"{self.binary_name} init -n --python {python_version}")

    def add(self, packages: list[str], dependency_type: str = "") -> None:
        packages_str = " ".join(packages)
        os.system(f"{self.binary_name} add {dependency_type} {packages_str}")

    def run(self, command: str) -> None:
        os.system(f"{self.binary_name} run {command}")


python_version = "{{ cookiecutter.python_version }}"

poetry = Poetry()
poetry.init(python_version)

base_pyproject_data = ""
with open("base_pyproject.toml") as f:
    base_pyproject_data = f.read().strip()
with open("pyproject.toml", "a+") as f:
    if base_pyproject_data:
        f.write("\n" + base_pyproject_data)
os.remove("base_pyproject.toml")

packages = [
    # formatting
    "black",
    "isort",

    # linting
    "flake8",
    "flake8-print",
    "pep8-naming",
    "mypy",
    "vulture",
    "bandit",

    # testing
    "pytest",
    "pytest-asyncio",
    "coverage",

    # debug
    "ipdb",

    # make
    "invoke",
]

poetry.add(packages, "-D")
poetry.run("invoke format")
