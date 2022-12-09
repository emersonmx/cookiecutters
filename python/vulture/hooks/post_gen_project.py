from pathlib import Path


def apply_snippet() -> None:
    snippet_path = Path("_pyproject_snippet.toml")
    with snippet_path.open() as f:
        snippet = f.readlines()

    pyproject_path = Path("pyproject.toml")
    if pyproject_path.exists():
        snippet.insert(0, "\n")
    with pyproject_path.open(mode="a") as f:
        f.writelines(snippet)

    snippet_path.unlink()


def main() -> int:
    apply_snippet()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
