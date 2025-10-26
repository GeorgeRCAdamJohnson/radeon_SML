FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .
COPY reasoning_agent.py .
COPY enhanced_search_utils.py .
COPY data/ ./data/
COPY src/react/deploy/ ./static/

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]