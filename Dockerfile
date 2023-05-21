FROM python:3.11-alpine

EXPOSE 8000

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install -r requirements.txt

COPY . /app

CMD ["sh", "entrypoint.sh"]