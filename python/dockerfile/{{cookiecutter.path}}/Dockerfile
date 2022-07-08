FROM python:{{ cookiecutter.docker_image_tag }} as build

WORKDIR /opt

RUN python -m venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH

COPY requirements.txt .
{%- if cookiecutter.require_hashes == "y" %}
RUN pip install --require-hashes -r requirements.txt
{%- else %}
RUN pip install -r requirements.txt
{%- endif %}


FROM python:{{ cookiecutter.docker_image_tag }}

RUN useradd --create-home appuser
USER appuser

WORKDIR /home/appuser

COPY --chown=appuser:appuser --from=build /opt/venv /home/appuser/venv
COPY --chown=appuser:appuser . /home/appuser/app

ENV PATH=/home/appuser/venv/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONOPTIMIZE=1 \
    PYTHONUNBUFFERED=1

CMD ["python", "app/main.py"]
