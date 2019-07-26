FROM python:3.6-alpine

WORKDIR /src

RUN apk add --no-cache gcc musl-dev linux-headers

COPY requirements.txt requirements.txt
COPY producer.py producer.py
COPY app.py app.py

RUN pip install --upgrade pip &&  pip install -r requirements.txt

CMD ["python", "app.py"]
