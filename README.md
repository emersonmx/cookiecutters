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

## Design Patterns

- All `python` templates has a `path` variable.
- Many `python` templates use a `post_gen_project.py` hook to apply a snippet.
