FROM python:3.9.0-slim-buster

ARG /usr/src/app

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get install -y gcc gettext-base && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN --mount=type=cache,target=/root/.cache/pip pip install -U pip && pip install --no-cache-dir -r requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt

COPY ./ ./

ARG SERVICE_NAME
ENV SERVICE_NAME ${SERVICE_NAME}

ENTRYPOINT ["./init.sh"]
