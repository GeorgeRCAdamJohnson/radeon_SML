@echo off
echo Stopping your app...
docker stop radeon-ai-app
docker rm radeon-ai-app
echo App stopped and removed!
pause