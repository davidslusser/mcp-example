# ---------- Stage 1: Builder ----------
FROM python:3.13-alpine AS builder

WORKDIR /app

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install build dependencies
RUN apk add --no-cache build-base

# Copy dependency file
COPY pyproject.toml .

# Install dependencies into a local directory (no system-wide install)
RUN pip install --upgrade pip && \
    pip install --prefix=/install .[docker]


# ---------- Stage 2: Runtime ----------
FROM python:3.13-alpine

ARG IMAGE_TAG=dev
ENV IMAGE_TAG=${IMAGE_TAG}

WORKDIR /app
ENV PYTHONPATH=/app

# Copy only the installed packages from builder
COPY --from=builder /install /usr/local

# Copy application source
COPY src/app/ /app/app/
COPY src/run.py /app/run.py

EXPOSE 8000
CMD ["python", "run.py"]
