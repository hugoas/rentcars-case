# Stage 1 - build
FROM python:3.10-slim as builder

WORKDIR /app

COPY . .

RUN pip install --user fastapi uvicorn pandas pyarrow prometheus-fastapi-instrumentator

# Stage 2 - runtime
FROM python:3.10-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]