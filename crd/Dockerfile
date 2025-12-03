FROM python:3.11-slim

WORKDIR /app

RUN pip install kopf kubernetes requests

COPY controller.py controller.py

CMD ["kopf", "run", "--standalone", "controller.py"]
