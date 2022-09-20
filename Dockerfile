FROM python:3.10

COPY ./alembic /test_task_fabrique/alembic
COPY ./api /test_task_fabrique/api
COPY ./tests /test_task_fabrique/tests
COPY ./requirements.txt /test_task_fabrique
COPY ./alembic.ini /test_task_fabrique

RUN pip3 install -r /test_task_fabrique/requirements.txt

EXPOSE 5050