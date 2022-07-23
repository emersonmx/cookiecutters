from invoke import Context, task


@task(aliases=("fmt",))
{%- if cookiecutter.use_pre_commit == "y" %}
def format(c, all_files=False):
    # type: (Context, bool) -> None
    precommit_options = []

    if all_files:
        precommit_options.append("--all-files")

    hooks = [
        "trailing-whitespace",
        "end-of-file-fixer",
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
    all_files = get_files(c, ".")
    py_files = get_files(c, "*.py")
    ipy_files = get_files(c, "*.ipy")

    c.run(f"trailing-whitespace-fixer {all_files}")
    c.run(f"end-of-file-fixer {all_files}")
    c.run(f"pyupgrade --py310-plus {py_files}")
    c.run(f"add-trailing-comma {py_files}")
    c.run(f"yesqa {py_files}")
    c.run(f"isort --filter-files {py_files} {ipy_files}".strip())
    c.run(f"black {py_files} {ipy_files}".strip())
{%- endif %}
