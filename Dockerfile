# ── Build stage ───────────────────────────────────────────────────────────────
# Use official slim Python image to keep the final image small
FROM python:3.11-slim

# Set environment variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing .pyc files
# PYTHONUNBUFFERED: Ensures stdout/stderr are sent directly to the terminal
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Copy and install dependencies first (leverages Docker layer caching)
# If requirements.txt hasn't changed, this layer is reused on rebuilds
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code
COPY app/ ./app/

# Expose the application port
EXPOSE 5000

# Run the app using gunicorn (production-grade WSGI server)
# -w 2          → 2 worker processes
# -b 0.0.0.0:5000 → listen on all interfaces at port 5000
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app.main:app"]
