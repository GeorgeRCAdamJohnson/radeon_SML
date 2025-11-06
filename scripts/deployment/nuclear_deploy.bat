@echo off
echo === NUCLEAR DEPLOYMENT ===
echo Deleting existing Cloud Run service...
gcloud run services delete radeon-ai --region us-central1 --quiet

echo Waiting 10 seconds...
timeout /t 10

echo Deploying fresh service...
gcloud run deploy radeon-ai --source . --platform managed --region us-central1 --allow-unauthenticated

echo === DEPLOYMENT COMPLETE ===
pause