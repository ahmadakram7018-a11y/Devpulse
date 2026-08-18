# Step 1 — Base image
# We start from official Python 3.11 slim image
# slim = smaller size, only essentials included
FROM python:3.11-slim

# Step 2 — Set working directory inside container
# All subsequent commands run from /app
WORKDIR /app

# Step 3 — Copy requirements first (for layer caching)
# If requirements don't change — pip install is cached
COPY requirements.txt .

# Step 4 — Install dependencies
# --no-cache-dir = don't cache pip downloads (smaller image)
RUN pip install --no-cache-dir -r requirements.txt

# Step 5 — Copy all application code
# This layer changes most often — put it last
COPY . .

# Step 6 — Expose port 8000
# Tells Docker this container uses port 8000
EXPOSE 8000

# Step 7 — Run the application
# host 0.0.0.0 = accept connections from outside container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]