from invoke import task
from invoke.context import Context


@task
def run(c):
    # type: (Context) -> None
    c.run("python src/main.py")


@task(aliases=["fmt"])
def format(c, all_files=False):
    # type: (Context, bool) -> None
    c.config["run"]["pty"] = True
    if all_files:
        c.run("pre-commit run --all-files pyupgrade")
        c.run("pre-commit run --all-files add-trailing-comma")
        c.run("pre-commit run --all-files isort")
        c.run("pre-commit run --all-files black")
    else:
        c.run("pre-commit run pyupgrade")
        c.run("pre-commit run add-trailing-comma")
        c.run("pre-commit run isort")
        c.run("pre-commit run black")


@task
def lint(c, all_files=False):
    # type: (Context, bool) -> None
    c.config["run"]["pty"] = True
    if all_files:
        c.run("pre-commit run --all-files flake8")
        c.run("pre-commit run --all-files mypy")
        c.run("pre-commit run --all-files vulture")
        c.run("pre-commit run --all-files bandit")
    else:
        c.run("pre-commit run flake8")
        c.run("pre-commit run mypy")
        c.run("pre-commit run vulture")
        c.run("pre-commit run bandit")


@task
def check(c, all_files=False):
    # type: (Context, bool) -> None
    c.config["run"]["pty"] = True
    if all_files:
        c.run("pre-commit run --all-files")
    else:
        c.run("pre-commit run")


@task
def tests(c):
    # type: (Context) -> None
    cmd = " ".join(
        [
            "PYTHONPATH=src/",
            "coverage",
            "run",
            "-m",
            "pytest",
            "tests/",
        ],
    )
    c.run(cmd, pty=True)


@task
def coverage(c):
    # type: (Context) -> None
    c.run("coverage report", pty=True)
