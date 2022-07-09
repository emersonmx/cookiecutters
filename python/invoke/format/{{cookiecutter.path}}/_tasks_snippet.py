from invoke import Context, task


@task(aliases=("fmt",))
{%- if cookiecutter.use_pre_commit == "y" %}
def format(c, all_files=False):
    # type: (Context, bool) -> None
    precommit_options = []

    if all_files:
        precommit_options.append("--all-files")

    hooks = [
        "end-of-file-fixer",
        "trailing-whitespace",
        "pyupgrade",
        "add-trailing-comma",
        "yesqa",
        "isort",
        "black",
    ]
    for hook in hooks:
        cmd = " ".join(["pre-commit", "run", *precommit_options, hook])
        c.run(cmd)
{%- else %}
def format(c):
    # type: (Context) -> None
    c.run("isort .")
    c.run("black .")
{%- endif %}
