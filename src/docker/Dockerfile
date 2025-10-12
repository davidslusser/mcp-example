FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Copy only the dependency file first (for caching)
COPY pyproject.toml .

# Install dependencies directly from pyproject.toml
RUN pip install --upgrade pip && \
    pip install .


# Now copy the app source
COPY src/app/ /app/app/
COPY src/run.py /app/run.py

EXPOSE 8000
CMD ["python", "run.py"]
