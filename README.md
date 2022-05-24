# cookiecutters

```sh
# Create a .envrc for poetry in current directory
cookiecutter \
  --no-input \
  -f \
  -o $(dirname $PWD) \
  https://github.com/emersonmx/cookiecutters --directory=direnv/poetry \
  path=$PWD
```

