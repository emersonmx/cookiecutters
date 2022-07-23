from invoke import Context, task


@task
{%- if cookiecutter.use_pre_commit == "y" %}
def lint(c, all_files=False):
    # type: (Context, bool) -> None
    precommit_options = []

    if all_files:
        precommit_options.append("--all-files")

    hooks = [
        "check-ast",
        "debug-statements",
        "name-tests-test",
        "check-merge-conflict",
        "check-added-large-files",
        "detect-private-key",
        "flake8",
        "mypy",
        "vulture",
        "bandit",
    ]
    for hook in hooks:
        cmd = " ".join(["pre-commit", "run", *precommit_options, hook])
        c.run(cmd)
{%- else %}
def lint(c):
    # type: (Context) -> None
    all_files = get_files(c, ".")
    source_files = get_files(c, "*.py", "^tests/")
    py_files = get_files(c, "*.py")
    ipy_files = get_files(c, "*.ipy")
    py_test_files = get_files(c, "tests/*.py")

    c.run(f"check-ast {py_files}")
    c.run(f"debug-statement-hook {py_files}")
    c.run(f"name-tests-test {py_test_files}")
    c.run(f"check-merge-conflict {all_files}")
    c.run(f"check-added-large-files {all_files}")
    c.run(f"detect-private-key {all_files}")
    c.run(f"flake8 {py_files}")
    c.run(f"mypy --strict {py_files} {ipy_files}".strip())
    c.run(f"vulture {py_files}")
    c.run(f"bandit -r {source_files}")
{%- endif %}
