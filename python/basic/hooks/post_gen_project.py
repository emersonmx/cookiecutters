import os
from subprocess import run, DEVNULL
from urllib.request import urlopen, Request

run(["poetry", "init", "-n", "--python", "^3.9"])

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
run(["poetry", "add", "-D", *packages])

run(["git", "init"])
run(["poetry", "run", "pre-commit", "install"])
run(["poetry", "run", "pre-commit", "autoupdate"], stdout=DEVNULL)

gitignore_url = "https://www.toptal.com/developers/gitignore/api/python"
headers = {"user-agent": "Mozilla/5.0"}
request = Request(gitignore_url, headers=headers)
with urlopen(request) as response:
    data = response.read()
    with open(".gitignore", "w+") as f:
        f.write(data.decode())

run(["git", "add", "."])
run(["git", "commit", "-m", "Start project"])
