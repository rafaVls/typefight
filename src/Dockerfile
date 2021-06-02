FROM python:3.9.5-slim-buster

WORKDIR /var/app/

COPY requirements.txt .
COPY typefight/ ./typefight/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["flask", "run"]