FROM python:{{ cookiecutter.docker_image_tag }} as venv

RUN python -m venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH

COPY requirements.txt /requirements.txt
RUN pip install --require-hashes -r requirements.txt


FROM python:{{ cookiecutter.docker_image_tag }}

RUN useradd --create-home appuser
USER appuser

WORKDIR /app

ENV PATH=/opt/venv/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONOPTIMIZE=1 \
    PYTHONUNBUFFERED=1

COPY --from=venv /opt/venv /opt/venv
COPY . .

CMD ["python", "main.py"]
