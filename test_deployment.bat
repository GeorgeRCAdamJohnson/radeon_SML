@echo off
echo Testing Radeon AI deployment...

echo Testing health endpoint...
curl -s http://localhost:8000/api/health
echo.

echo Testing status endpoint...
curl -s http://localhost:8000/api/status
echo.

echo Testing chat endpoint with Gundam query...
curl -X POST http://localhost:8000/api/chat -H "Content-Type: application/json" -d "{\"message\": \"What is Gundam?\", \"format\": \"detailed\"}"
echo.

echo Testing chat endpoint with Data query...
curl -X POST http://localhost:8000/api/chat -H "Content-Type: application/json" -d "{\"message\": \"Tell me about Data from Star Trek\", \"format\": \"detailed\"}"
echo.

echo All tests completed!
pause