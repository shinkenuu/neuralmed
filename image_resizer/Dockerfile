FROM python:3.6-alpine

WORKDIR /src

RUN apk --update add build-base jpeg-dev zlib-dev

COPY requirements.txt requirements.txt
COPY app.py app.py

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "app.py"]
