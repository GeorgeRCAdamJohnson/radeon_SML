@echo off
echo Restarting Docker Desktop and deploying...

echo Killing Docker processes...
taskkill /F /IM "Docker Desktop.exe" 2>nul
taskkill /F /IM "dockerd.exe" 2>nul
taskkill /F /IM "com.docker.backend.exe" 2>nul

echo Waiting for processes to stop...
timeout /t 5 >nul

echo Starting Docker Desktop...
start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"

echo Waiting for Docker to start...
timeout /t 30 >nul

echo Checking Docker status...
docker --version

echo Stopping any existing containers...
docker-compose down 2>nul

echo Building new image...
docker-compose build

echo Starting services...
docker-compose up -d

echo Deployment complete!
echo Service available at: http://localhost:8000

pause