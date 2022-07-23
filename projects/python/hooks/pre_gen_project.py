import re


def main() -> int:
    pattern = r"^[_a-zA-Z][_a-zA-Z0-9]+$"
    module_name = "{{ cookiecutter.project_slug }}"
    if re.match(pattern, module_name):
        return 0

    message = [
        f"ERROR: The project slug {module_name} is not a valid Python module name.",  # noqa
        "Please do not use a - and use _ instead",
    ]
    print("\n".join(message))  # noqa

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
