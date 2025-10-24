FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python server and reasoning agent
COPY server.py .
COPY reasoning_agent.py .
COPY server_enhanced.py .

# Copy React frontend
COPY src/react/deploy ./static

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Expose port
EXPOSE 8000

# Start server with static file serving
CMD ["python", "-u", "server_enhanced.py"]