FROM python:3.7-slim

WORKDIR /app

COPY ./requirements.txt /app

RUN pip install -r requirements.txt --no-cache-dir

COPY ./foodgram/ /app

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]