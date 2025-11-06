@echo off
echo Checking Radeon AI container status...

echo Docker containers:
docker ps --filter "name=radeon"

echo.
echo Service health:
curl -s http://localhost:8000/api/health | python -m json.tool 2>nul || echo "Service not responding"

echo.
echo Service status:
curl -s http://localhost:8000/api/status | python -m json.tool 2>nul || echo "Status endpoint not available"

pause