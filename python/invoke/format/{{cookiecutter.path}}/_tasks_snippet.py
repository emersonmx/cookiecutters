from invoke import Context, task


@task(aliases=("fmt",))
def format(c, all_files=False):
    {%- if cookiecutter.use_pre_commit %}
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
        c.run(cmd, pty=True)
    {%- else %}
    c.run("isort .")
    c.run("black .")
    {%- endif %}
