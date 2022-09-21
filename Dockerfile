FROM python:3.10.7-slim-buster


WORKDIR /usr/src/test_task_fabrique

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .

RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean

RUN pip install --upgrade pip

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5050