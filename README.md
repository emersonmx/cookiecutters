# cookiecutters

## Examples

```sh
# Create a python template into current project
cookiecutter \
    --directory=python/direnv \
    https://github.com/emersonmx/cookiecutters.git \
    path=$PWD
```

```sh
# Create a python project
# With cocu: https://github.com/emersonmx/dotfiles/blob/main/dot_local/bin/executable_cocu
virtualenv .venv \
    && git init \
    && cocu \
        python/{direnv,editorconfig,build-system,project-setup,devdeps,pre-commit,isort,black,flake8,mypy,vulture} \
        --context project_name=$(basename $PWD)

# Without cocu
virtualenv .venv \
    && git init \
    && echo \
        python/{direnv,editorconfig,build-system,project-setup,devdeps,pre-commit,isort,black,flake8,mypy,vulture} \
            | xargs -d' ' -I {} \
                cookiecutter \
                    -f \
                    --no-input \
                    https://github.com/emersonmx/cookiecutters.git \
                    --directory {} \
                    path=$PWD project_name=$(basename $PWD)
```

## Design Decisions

- Language templates MUST HAVE a `path` variable.
- Use python to write the hooks.
- Use only the standard and cookiecutter libraries to write the hooks.
- Templates MUST FOLLOW good design decisions (use tests, dev tools, etc).
