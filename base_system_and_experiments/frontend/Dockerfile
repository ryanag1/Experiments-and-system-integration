FROM node:lts-alpine3.12

RUN apk add git python3 make g++

WORKDIR /
COPY package.json* ./
RUN --mount=type=cache,target=/root/.npm npm install

ARG /app
WORKDIR /app

COPY ./ ./

ARG SERVICE_NAME
ENV SERVICE_NAME ${SERVICE_NAME}

ENTRYPOINT ["./init-dev.sh"]
