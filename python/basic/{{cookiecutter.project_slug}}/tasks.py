from invoke import Context, task


@task
def run(c):
    # type: (Context) -> None
    c.run("python src/main.py")


@task(aliases=["fmt"])
def format(c, all_files=False):
    # type: (Context, bool) -> None
    c.config["run"]["pty"] = True
    hooks = [
        "pyupgrade",
        "add-trailing-comma",
        "yesqa",
        "isort",
        "black",
    ]
    cmd = "pre-commit run --all-files" if all_files else "pre-commit run"
    for hook in hooks:
        c.run(f"{cmd} {hook}")


@task
def lint(c, all_files=False):
    # type: (Context, bool) -> None
    c.config["run"]["pty"] = True
    hooks = [
        "flake8",
        "mypy",
        "vulture",
        "bandit",
    ]
    cmd = "pre-commit run --all-files" if all_files else "pre-commit run"
    for hook in hooks:
        c.run(f"{cmd} {hook}")


@task
def check(c, all_files=False):
    # type: (Context, bool) -> None
    c.config["run"]["pty"] = True
    cmd = "pre-commit run --all-files" if all_files else "pre-commit run"
    c.run(cmd)


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
