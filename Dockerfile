FROM python:3.12

WORKDIR /server

RUN mkdir code
COPY ./requirements.txt /server/requirements.txt
RUN pip install -r /server/requirements.txt
