# syntax=docker/dockerfile:1
FROM python:3.9
RUN apt-get update && pip install --upgrade pip
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=80", "--reload"]