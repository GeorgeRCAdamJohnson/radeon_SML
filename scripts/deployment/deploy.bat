@echo off
echo Deploying to Google Cloud Run...

REM Build and deploy to Google Cloud Run
gcloud run deploy radeon-ai ^
  --source . ^
  --platform managed ^
  --region us-central1 ^
  --allow-unauthenticated ^
  --port 8000 ^
  --memory 1Gi ^
  --cpu 1 ^
  --timeout 300 ^
  --max-instances 10

echo Deployment complete!
pause