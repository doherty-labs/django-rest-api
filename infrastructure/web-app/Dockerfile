FROM node:23
EXPOSE 3000
ARG WEBAPP_PATH

ARG NEXT_PUBLIC_DATADOG_VERSION
ENV NEXT_PUBLIC_DATADOG_VERSION=${NEXT_PUBLIC_DATADOG_VERSION}

ARG APP_ENV
ENV APP_ENV=${APP_ENV}

ARG OP_SERVICE_ACCOUNT_TOKEN
ENV OP_SERVICE_ACCOUNT_TOKEN=${OP_SERVICE_ACCOUNT_TOKEN}

RUN ARCH="amd64"; \
    OP_VERSION="v$(curl https://app-updates.agilebits.com/check/1/0/CLI2/en/2.0.0/N -s | grep -Eo '[0-9]+\.[0-9]+\.[0-9]+')"; \
    curl -sSfo op.zip \
    https://cache.agilebits.com/dist/1P/op2/pkg/"$OP_VERSION"/op_linux_"$ARCH"_"$OP_VERSION".zip \
    && unzip -od /usr/local/bin/ op.zip \
    && rm op.zip

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

WORKDIR /usr/src/app

COPY ${WEBAPP_PATH}/package*.json ./web-app/
COPY ${WEBAPP_PATH}/pnpm-lock.yaml ./web-app/

WORKDIR /usr/src/app/web-app/
RUN pnpm install

COPY ${WEBAPP_PATH} ./
COPY ./infrastructure/web-app/entry.sh /usr/src/app/

COPY ./infrastructure/web-app/env_files.sh /usr/src/app/
RUN ["chmod", "+x", "/usr/src/app/env_files.sh"]
RUN /usr/src/app/env_files.sh

RUN pnpm build

RUN ["chmod", "+x", "/usr/src/app/entry.sh"]
ENTRYPOINT ["/usr/src/app/entry.sh"]