@echo off
echo Installing Docker Desktop is required first!
echo.
echo 1. Download Docker Desktop from: https://www.docker.com/products/docker-desktop/
echo 2. Install and restart your computer
echo 3. Run this script again
echo.
pause

echo Building your app...
docker build -t radeon-ai .

echo Starting your app...
docker run -d -p 8000:8000 --name radeon-ai-app radeon-ai

echo.
echo Done! Your app is running at: http://localhost:8000
echo.
echo To stop: docker stop radeon-ai-app
echo To restart: docker start radeon-ai-app
pause