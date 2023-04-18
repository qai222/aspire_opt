FROM python:3.10-slim AS base
RUN apt-get update \
    && apt-get upgrade -y \
    && apt install -y build-essential \
    && apt-get autoremove -y

WORKDIR /home/code
COPY requirements.txt ./requirements.txt
COPY app/ ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt
