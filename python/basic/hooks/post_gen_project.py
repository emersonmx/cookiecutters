import os
from subprocess import run, DEVNULL

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

run(
    [
        "curl",
        "--location",
        "--output",
        ".gitignore",
        "https://www.toptal.com/developers/gitignore/api/python",
    ]
)

run(["git", "add", "."])
run(["git", "commit", "-m", "Start project"])
