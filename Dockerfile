# Python 3.11 base image
FROM python:3.11-slim

# Working directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Run the bot
CMD ["python", "main.py"]

