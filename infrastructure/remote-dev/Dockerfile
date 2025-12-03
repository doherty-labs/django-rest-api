FROM python:3.14.1

EXPOSE 8000
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

RUN apt-get update
RUN apt-get install -y apt-transport-https curl software-properties-common
RUN curl -sL https://deb.nodesource.com/setup_20.x | bash -

RUN apt-get install -y nodejs 
RUN npm install --global prettier
RUN apt-get install nano -y
RUN apt-get install vim -y
RUN npm install -g pnpm
RUN pnpm config set store-dir /home/node/.local/share/pnpm/store

RUN pip install --upgrade pip
RUN pip install setuptools wheel
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /usr/src/app
COPY ./ /usr/src/app/

WORKDIR /usr/src/app/api/django_project
RUN poetry env use python3.13
RUN poetry config virtualenvs.create true
RUN poetry config virtualenvs.in-project false
RUN poetry install

RUN npm install -g openapi-typescript
RUN pip install openapi-generator-cli[jdk4py]
RUN pip install pre-commit

WORKDIR /usr/src/app
RUN mkdir -p /logs/
RUN mkdir -p /usr/src/app/tempFileStore/

ENTRYPOINT ["tail"]
CMD ["-f","/dev/null"]
