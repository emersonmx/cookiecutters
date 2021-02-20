from invoke import task
from invoke.context import Context


{% if cookiecutter.install_code_tools == "y" -%}
@task
def format(c):
    # type: (Context) -> None
    c.run("black .")
    c.run("isort .")


@task
def lint(c):
    # type: (Context) -> None
    c.run("flake8 .")
    c.run("mypy .")
{%- endif -%}

{% if cookiecutter.install_test_tools == "y" -%}
{%- if cookiecutter.install_code_tools == "y" %}


{% endif -%}
@task
def tests(c):
    # type: (Context) -> None
    c.run("coverage run -m pytest .")


@task
def coverage(c):
    # type: (Context) -> None
    c.run("coverage report")
{%- endif -%}
