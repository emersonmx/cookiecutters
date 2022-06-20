from invoke import Context, task


@task
def run(c):
    # type: (Context) -> None
    c.run("{{ cookiecutter.command }}", pty=True)
