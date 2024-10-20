FROM python:3.13.0

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
  POETRY_VERSION=1.4.1

RUN apt-get update
RUN apt-get install -y apt-transport-https curl software-properties-common
RUN curl -sL https://deb.nodesource.com/setup_20.x | bash -

RUN apt-get install -y nodejs 
RUN npm install --global yarn
RUN npm install --global prettier
RUN apt-get install nano -y
RUN apt-get install vim -y
RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false


WORKDIR /usr/src/app
COPY ./ /usr/src/app/

WORKDIR /usr/src/app/api/django_project
RUN poetry install
RUN playwright install-deps
RUN playwright install

RUN npm install -g openapi-typescript@7.0.2

WORKDIR /usr/src/app/web-app/merchant
RUN yarn install

WORKDIR /usr/src/app/web-app/ops
RUN yarn install

WORKDIR /usr/src/app/web-app/storefront
RUN yarn install

WORKDIR /usr/src/app
RUN mkdir -p /logs/

ENTRYPOINT ["tail"]
CMD ["-f","/dev/null"]
