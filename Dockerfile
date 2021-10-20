FROM python:3

ENV PYTHONBUFFERED=1

WORKDIR /code_1

ADD . /code_1

COPY ./requirements.txt /code_1/requirements.txt

RUN pip install -r requirements.txt

COPY . /code_1