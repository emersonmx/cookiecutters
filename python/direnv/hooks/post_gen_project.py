import uuid
from subprocess import CalledProcessError


def apply_cache_buster() -> None:
    lines = [
        "\n",
        f"# Cache buster: {uuid.uuid4()}\n",
    ]
    with open(".envrc", "a") as f:
        f.writelines(lines)


def main() -> int:
    try:
        apply_cache_buster()
    except CalledProcessError:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
