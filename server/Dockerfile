FROM python:3.8

WORKDIR /server/
COPY . .

RUN pip install fastapi "uvicorn[standard]" psycopg2
