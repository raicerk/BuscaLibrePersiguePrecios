FROM python:alpine

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev 

LABEL Name=buscalibrewebscrapingprecios Version=0.0.1

WORKDIR /app

ADD . /app

RUN python3 -m pip install -r requirements.txt

RUN ["chmod", "+x", "./wait-for-postgres.sh"]

CMD ["./wait-for-postgres.sh", "python3", "/app/app.py"]
