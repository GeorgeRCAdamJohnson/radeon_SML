#!/bin/bash

echo "Building Docker image..."
docker build -t radeon-ai .

echo "Running container..."
docker run -d -p 8000:8000 --name radeon-ai-container radeon-ai

echo "Container started! Access at http://localhost:8000"