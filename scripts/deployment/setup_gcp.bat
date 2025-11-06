@echo off
echo Setting up Google Cloud Project...
echo.

echo Creating new project...
gcloud projects create radeon-ai-kb-2024 --name="Radeon AI Knowledge Base"

echo Setting project...
gcloud config set project radeon-ai-kb-2024

echo Enabling required APIs...
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com

echo Setup complete! Now run deploy_gcp.bat
pause