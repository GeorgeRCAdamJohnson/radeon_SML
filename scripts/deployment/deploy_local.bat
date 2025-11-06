@echo off
echo Building and deploying Radeon AI locally...

echo Stopping any existing containers...
docker-compose down

echo Building new image...
docker-compose build

echo Starting services...
docker-compose up -d

echo Waiting for service to start...
timeout /t 5

echo Testing health endpoint...
curl -s http://localhost:8000/api/health

echo.
echo Deployment complete! 
echo Access the service at: http://localhost:8000
echo API health check: http://localhost:8000/api/health
echo API status: http://localhost:8000/api/status

pause