FROM python:3.9-slim

WORKDIR /src

RUN apt-get update -y && apt-get upgrade -y && apt-get install vim -y
RUN apt-get install -y curl net-tools

COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application files
COPY . .

EXPOSE 80
ENTRYPOINT uvicorn src:app --reload --port 8080
