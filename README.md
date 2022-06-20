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

## Design Decisions

- All language templates MUST BE project agnostic.
- All language templates MUST HAVE a `path` variable.
- The responsibility for modifying the language templates rests with the
  project templates.
- Use python to write the hooks.
- Use only the standard, requests and cookiecutter libraries to write the
  hooks.
- Many language templates use a `post_gen_project.py` hook to apply a snippet.
