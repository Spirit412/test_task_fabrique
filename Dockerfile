FROM python:3.10.7-alpine


WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /usr/src/app/requirements.txt


RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
        libressl-dev libffi-dev gcc musl-dev python3-dev \
        postgresql-dev \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r /usr/src/app/requirements.txt \
    && rm -rf /root/.cache/pip


# RUN apt-get update \
#   && apt-get -y install netcat gcc postgresql \
#   && apt-get clean

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . ./usr/src/app

EXPOSE 5050