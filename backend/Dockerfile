FROM python:3.11-slim

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Leverage Docker layer caching for deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY app ./app

# Expose uvicorn port
ENV PORT=8080
EXPOSE 8080

# For pydantic settings and any runtime envs
ENV PYTHONUNBUFFERED=1

# Healthcheck (optional; Fly also has internal checks)
HEALTHCHECK CMD curl -f http://localhost:8080/health || exit 1

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8080"]



