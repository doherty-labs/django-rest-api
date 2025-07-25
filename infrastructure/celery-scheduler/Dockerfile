FROM python:3.13.5

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.8.4

RUN pip install --upgrade pip
RUN pip install setuptools wheel
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /usr/src/app
COPY ./api/django_project/poetry.lock ./api/django_project/pyproject.toml /usr/src/app/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

WORKDIR /usr/src/app
COPY ./api/django_project ./django
COPY ./infrastructure/celery-scheduler/entry.sh ./
RUN mkdir -p /logs/
RUN mkdir -p /usr/src/app/tempFileStore/

RUN ["chmod", "+x", "./entry.sh"]
ENTRYPOINT ["./entry.sh"]