from pathlib import Path


def get_snippet_path() -> Path:
    return Path("_pyproject_snippet.toml")


def get_requirements_path() -> Path:
    return Path("requirements-dev.in")


def apply_snippet() -> None:
    snippet_path = get_snippet_path()
    with snippet_path.open() as f:
        snippet = f.readlines()

    pyproject_path = Path("pyproject.toml")
    if pyproject_path.exists():
        snippet.insert(0, "\n")
    with pyproject_path.open(mode="a") as f:
        f.writelines(snippet)


def setup_requirements() -> None:
    snippet_path = get_snippet_path()
    snippet_path.unlink()


def setup_pyproject() -> None:
    apply_snippet()
    requirements_path = get_requirements_path()
    requirements_path.unlink()
    snippet_path = get_snippet_path()
    snippet_path.unlink()


def main() -> int:
    format = "{{ cookiecutter.format }}".strip().lower()
    if format == "requirements":
        setup_requirements()
    else:
        setup_pyproject()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
