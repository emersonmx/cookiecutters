from invoke import task
from invoke.context import Context


@task
def run(c):
    # type: (Context) -> None
    c.run("python src/main.py")


@task(aliases=["fmt"])
def format(c):
    # type: (Context) -> None
    c.config["run"]["pty"] = True
    c.run("pre-commit run isort")
    c.run("pre-commit run black")


@task
def lint(c):
    # type: (Context) -> None
    c.config["run"]["pty"] = True
    c.run("pre-commit run flake8")
    c.run("pre-commit run mypy")
    c.run("pre-commit run vulture")
    c.run("pre-commit run bandit")


@task
def check(c):
    # type: (Context) -> None
    c.run("pre-commit run --all-files", pty=True)


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
