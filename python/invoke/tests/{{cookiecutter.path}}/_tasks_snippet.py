from invoke import Context, task


@task
def tests(c, quiet=False):
    # type: (Context, bool) -> None
    pytest_options: list[str] = []

    if quiet:
        pytest_options.append("-q")

    cmd = " ".join(
        [
            "coverage",
            "run",
            "-m",
            "pytest",
            *pytest_options,
        ],
    )
    c.run(cmd)


@task
def coverage(c):
    # type: (Context) -> None
    c.run("coverage report")
