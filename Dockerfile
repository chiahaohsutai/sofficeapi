FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y \
    libreoffice \
    libreoffice-script-provider-python \
    default-jre \
    python3-uno \
    fonts-dejavu \
    fonts-liberation \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN /usr/local/bin/pip3 install unoserver && \
    sed -i '1s;^;#!/usr/bin/env python3\n;' /usr/local/lib/python3.12/site-packages/unoserver/server.py && \
    chmod +x /usr/local/lib/python3.12/site-packages/unoserver/server.py

ENV PYTHONPATH=/usr/lib/python3/dist-packages

WORKDIR /sofficeapi

COPY . .
RUN /usr/local/bin/python3 -m venv .venv && \
    . .venv/bin/activate && \
    pip install --upgrade pip && \
    pip install uv && \
    uv sync --no-dev

ENV PYTHONUNBUFFERED=1
ENV SOFFICE_PYTHON=/usr/local/bin/python3
ENV SAL_USE_VCLPLUGIN=svp
ENV DISPLAY=:0

EXPOSE 8080
CMD ["./.venv/bin/python3", "-m", "uvicorn", "src.app:app", "--log-level", "info", "--port", "8000", "--host", "0.0.0.0"]