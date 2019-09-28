FROM python:3.7.4-slim-buster
ADD requirements.txt /app/
ADD bot.py /app/
ADD headless.py /app/
WORKDIR /app
RUN pip install -r requirements.txt
