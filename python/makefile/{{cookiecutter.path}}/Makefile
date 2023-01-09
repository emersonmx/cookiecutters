_OLD_PATH := $(PATH)
VENV_DIR := {{ cookiecutter.venv_path }}
VIRTUAL_ENV := $(PWD)/$(VENV_DIR)
PATH := $(VIRTUAL_ENV)/bin:$(PATH)

.PHONY: setup
{%- if cookiecutter.package_manager == "pip-tools" %}
setup: pip-sync
{%- elif cookiecutter.package_manager == "pip" %}
setup: pip-install
{%- endif %}

$(VENV_DIR):
	@PATH="${_OLD_PATH}"
	python -m venv $@
{%- if cookiecutter.package_manager == "pip-tools" %}
	@PATH="${VIRTUAL_ENV}/bin:${PATH}"
	python -m pip install pip-tools

.PHONY: pip-compile
pip-compile: $(VENV_DIR)
	python -m piptools compile \
		--generate-hashes \
		-o requirements.txt \
		pyproject.toml

.PHONY: pip-sync
pip-sync: $(VENV_DIR)
	python -m piptools sync requirements.txt
{%- elif cookiecutter.package_manager == "pip" %}

.PHONY: pip-install
pip-install: $(VENV_DIR)
	pip install -r requirements.txt
{%- endif %}

.PHONY: run
run: $(VENV_DIR)
	python main.py

.PHONY: clean
clean:
	rm -rf $(VENV_DIR)
