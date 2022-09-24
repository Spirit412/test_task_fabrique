FROM python:3.10.7

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

COPY ./alembic /usr/src/app/alembic
COPY ./api /usr/src/app/api
COPY ./requirements.txt /usr/src/app
COPY ./alembic.ini /usr/src/app/alembic.ini
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /usr/src/app/requirements.txt
COPY . ./usr/src/app


EXPOSE 5050