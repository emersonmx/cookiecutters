# cookiecutters

## Example

```sh
# Create a python project
cookiecutter \
    --directory=projects/python \
    https://github.com/emersonmx/cookiecutters.git
```

```sh
# Create a python template into current project
cookiecutter \
    --directory=python/direnv \
    https://github.com/emersonmx/cookiecutters.git \
    path=$PWD
```

```sh
# cocu: https://github.com/emersonmx/dotfiles/blob/main/dot_local/bin/executable_cocu
virtualenv .venv \
    && git init \
    && cocu \
        python/{devdeps,direnv,editorconfig,pre-commit,pyproject/build-system,isort,black,flake8,mypy,vulture}
```

## Design Decisions

- Language templates MUST BE bricks to build a project template.
- Language templates MUST HAVE a `path` variable.
- The responsibility for modifying the language templates rests with the
  project templates.
- Use python to write the hooks.
- Use only the standard and cookiecutter libraries to write the hooks.
- A project MUST USE tools to help development (git, devdeps, pre-commit, etc).
- Templates MUST FOLLOW good design decisions (use tests, dev tools, etc).
