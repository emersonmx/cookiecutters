import os
import shutil
import subprocess
import urllib.request


class Poetry:
    def __init__(self) -> None:
        self.binary_name = "poetry"
        if not shutil.which(self.binary_name):
            raise RuntimeError("Poetry not found")

    def init(self, python_version: str) -> None:
        subprocess.run(
            [self.binary_name, "init", "-n", "--python", python_version]
        )

    def add(self, packages: list[str], dependency_type: str = "") -> None:
        cmd = [self.binary_name, "add"]
        if dependency_type == "dev":
            cmd.append("-D")
        subprocess.run(cmd + packages)

    def run(self, command: list[str]) -> None:
        subprocess.run([self.binary_name, "run", *command])


poetry = Poetry()
poetry.init("{{ cookiecutter.python_version }}")

base_pyproject_data = ""
with open("base_pyproject.toml") as f:
    base_pyproject_data = f.read().strip()
with open("pyproject.toml", "a+") as f:
    if base_pyproject_data:
        f.write("\n" + base_pyproject_data + "\n")
os.remove("base_pyproject.toml")

packages = [
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
    "pytest-asyncio",
    "coverage",
    # debug
    "ipdb",
    # make
    "invoke",
    # misc
    "pre-commit",
]

poetry.add(packages, "dev")

subprocess.run(["git", "init"])
subprocess.run(["poetry", "run", "pre-commit", "install"])
subprocess.run(
    ["poetry", "run", "pre-commit", "autoupdate"],
    stdout=subprocess.DEVNULL,
)

gitignore_url = "https://www.toptal.com/developers/gitignore/api/python"
headers = {"user-agent": "Mozilla/5.0"}
request = urllib.request.Request(gitignore_url, headers=headers)
with urllib.request.urlopen(request) as response:
    data = response.read()
    with open(".gitignore", "w+") as f:
        f.write(data.decode())

subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", "Start project"])
