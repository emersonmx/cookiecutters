from invoke import Context, task


@task
{%- if cookiecutter.use_pre_commit == "y" %}
def lint(c, all_files=False):
    # type: (Context, bool) -> None
    precommit_options = []

    if all_files:
        precommit_options.append("--all-files")

    hooks = [
        "check-added-large-files",
        "check-merge-conflict",
        "debug-statements",
        "detect-private-key",
        "name-tests-test",
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
    c.run("flake8 .")
    c.run("mypy --strict .")
    c.run("vulture .")
    c.run("bandit -r .")
{%- endif %}
