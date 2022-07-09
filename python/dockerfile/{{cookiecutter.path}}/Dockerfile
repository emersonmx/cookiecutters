FROM python:{{ cookiecutter.docker_image_tag }} as build

WORKDIR /home/appuser

RUN python -m venv /home/appuser/venv
ENV PATH=/home/appuser/venv/bin:$PATH

COPY requirements.txt .
RUN pip install -r requirements.txt


FROM python:{{ cookiecutter.docker_image_tag }}

RUN useradd --create-home appuser
USER appuser

WORKDIR /home/appuser/app

COPY --chown=appuser:appuser --from=build /home/appuser/venv /home/appuser/venv
COPY --chown=appuser:appuser . /home/appuser/app

ENV PATH=/home/appuser/venv/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONOPTIMIZE=1 \
    PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
