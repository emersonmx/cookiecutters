from invoke import Context, task


@task
def run(c):
    # type: (Context) -> None
    c.run("python src/main.py", pty=True)


@task(aliases=["fmt"])
def format(c, all_files=False):
    # type: (Context, bool) -> None
    precommit_options = []

    if all_files:
        precommit_options.append("--all-files")

    hooks = [
        "pyupgrade",
        "add-trailing-comma",
        "yesqa",
        "isort",
        "black",
    ]
    for hook in hooks:
        cmd = " ".join(["pre-commit", "run", *precommit_options, hook])
        c.run(cmd, pty=True)


@task
def lint(c, all_files=False):
    # type: (Context, bool) -> None
    precommit_options = []

    if all_files:
        precommit_options.append("--all-files")

    hooks = [
        "flake8",
        "mypy",
        "vulture",
        "bandit",
    ]
    for hook in hooks:
        cmd = " ".join(["pre-commit", "run", *precommit_options, hook])
        c.run(cmd, pty=True)


@task
def check(c, all_files=False):
    # type: (Context, bool) -> None
    precommit_options = []

    if all_files:
        precommit_options.append("--all-files")

    cmd = " ".join(["pre-commit", "run", *precommit_options])
    c.run(cmd, pty=True)


@task
def tests(c, quiet=False):
    # type: (Context, bool) -> None
    pytest_options: list[str] = []

    if quiet:
        pytest_options.append("-q")

    cmd = " ".join(
        [
            "PYTHONPATH=src/",
            "coverage",
            "run",
            "-m",
            "pytest",
            *pytest_options,
            "tests/",
        ],
    )
    c.run(cmd, pty=True)


@task
def coverage(c):
    # type: (Context) -> None
    c.run("coverage report", pty=True)
