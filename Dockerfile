FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir .

COPY src/ src/
COPY config.yaml .

VOLUME /app/src/guides
VOLUME /app/chroma_db

ENV CONFIG_PATH=/app/config.yaml

ENTRYPOINT ["python3", "src/server.py"]
