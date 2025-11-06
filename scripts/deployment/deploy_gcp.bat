@echo off
echo Google Cloud Run Deployment
echo.
echo 1. Install Google Cloud CLI: https://cloud.google.com/sdk/docs/install
echo 2. Run: gcloud auth login
echo 3. Run setup_gcp.bat to create project
echo 4. Run this script again
echo.
pause

echo Building and deploying to Google Cloud Run...
gcloud run deploy radeon-ai --source . --platform managed --region us-central1 --allow-unauthenticated

echo.
echo Deployment complete! Your app URL will be shown above.
pause