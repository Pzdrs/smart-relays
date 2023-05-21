FROM arm32v7/python:3

EXPOSE 8000

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install -r requirements.txt

COPY . /app

CMD ["sh", "entrypoint.sh"]