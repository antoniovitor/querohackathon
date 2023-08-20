# ---- Base python ----
FROM python:3.10.6-slim-buster as base

RUN mkdir -p /opt/ultron/dependencies
WORKDIR /opt/ultron
RUN apt update && apt upgrade -y
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt

# --- Release with Alpine ----
FROM base AS release
RUN mkdir -p /opt/ultron/src
WORKDIR /opt/ultron
COPY ./src ./src/