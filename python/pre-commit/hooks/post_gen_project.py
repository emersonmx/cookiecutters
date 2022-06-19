from subprocess import DEVNULL, CalledProcessError, run


def main() -> int:
    try:
        run(["pre-commit", "autoupdate"], stderr=DEVNULL)
    except CalledProcessError:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
