from invoke import task
from invoke.context import Context

src_path = "src/"
tests_path = "tests/"
tasks_path = "tasks.py"
format_paths = " ".join([src_path, tests_path, tasks_path])


@task
def run(c):
    # type: (Context) -> None
    c.run("python src/main.py")


@task(aliases=["fmt"])
def format(c):
    # type: (Context) -> None
    c.run(f"black {format_paths}")
    c.run(f"isort {format_paths}")


@task
def check_format(c):
    # type: (Context) -> None
    c.run(f"black --check --diff {format_paths}")
    c.run(f"isort --check --diff {format_paths}")


@task
def lint(c):
    # type: (Context) -> None
    paths = f"{src_path} {tasks_path}"
    c.run(f"flake8 {paths}")
    c.run(f"dmypy run {paths}")
    c.run(f"vulture {src_path}")
    c.run(f"bandit -r {src_path}")


@task
def tests(c):
    # type: (Context) -> None
    cmd = " ".join(
        [
            f"PYTHONPATH={src_path}",
            "coverage",
            "run",
            "-m",
            "pytest",
            tests_path,
        ]
    )
    c.run(cmd, pty=True)


@task
def coverage(c):
    # type: (Context) -> None
    c.run("coverage report", pty=True)


@task(check_format, lint, tests, coverage)
def check(c):
    # type: (Context) -> None
    pass
