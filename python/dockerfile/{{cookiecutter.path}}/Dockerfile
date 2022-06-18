FROM python:{{ cookiecutter.docker_image_tag }} as build

WORKDIR /usr/app

RUN python -m venv /usr/app/venv
ENV PATH=/usr/app/venv/bin:$PATH

COPY requirements.txt .
{%- if cookiecutter.require_hashes == "y" %}
RUN pip install --require-hashes -r requirements.txt
{%- else %}
RUN pip install -r requirements.txt
{%- endif %}


FROM python:{{ cookiecutter.docker_image_tag }}

RUN useradd --create-home python
USER python

WORKDIR /usr/app

COPY --chown=python:python --from=build /usr/app/venv /usr/app/venv
COPY --chown=python:python . /usr/app

ENV PATH=/usr/app/venv/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONOPTIMIZE=1 \
    PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
