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
