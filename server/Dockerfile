FROM python:3.5

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /server
WORKDIR /server

COPY . /server

EXPOSE 31337

CMD ["python3", "server.py"]