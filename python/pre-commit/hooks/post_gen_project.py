import subprocess
from functools import partial

run = partial(subprocess.run, check=True)


def main() -> int:
    try:
        run(["pre-commit", "autoupdate"])
    except subprocess.CalledProcessError:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
