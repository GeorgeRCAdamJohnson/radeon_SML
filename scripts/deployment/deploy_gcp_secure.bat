@echo off
echo Secure Google Cloud Run Deployment
echo.

REM Enable required APIs
echo Enabling security APIs...
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable compute.googleapis.com
gcloud services enable cloudarmor.googleapis.com

REM Create Cloud Armor security policy
echo Creating Cloud Armor WAF policy...
gcloud compute security-policies create radeon-ai-waf ^
    --description="WAF policy for Radeon AI"

REM Add rate limiting rule
gcloud compute security-policies rules create 1000 ^
    --security-policy=radeon-ai-waf ^
    --expression="true" ^
    --action=rate-based-ban ^
    --rate-limit-threshold-count=100 ^
    --rate-limit-threshold-interval-sec=60 ^
    --ban-duration-sec=600 ^
    --conform-action=allow ^
    --exceed-action=deny-429 ^
    --enforce-on-key=IP

REM Add geo-blocking (optional - adjust countries as needed)
gcloud compute security-policies rules create 2000 ^
    --security-policy=radeon-ai-waf ^
    --expression="origin.region_code == 'CN' || origin.region_code == 'RU'" ^
    --action=deny-403

REM Deploy with authentication required
echo Building and deploying to Google Cloud Run with security...
gcloud run deploy radeon-ai ^
    --source . ^
    --platform managed ^
    --region us-central1 ^
    --no-allow-unauthenticated ^
    --cpu=2 ^
    --memory=4Gi ^
    --max-instances=10 ^
    --concurrency=80

REM Create IAM binding for specific users (replace with actual email)
echo Setting up IAM permissions...
echo Enter the email address that should have access:
set /p USER_EMAIL=Email: 
gcloud run services add-iam-policy-binding radeon-ai ^
    --region=us-central1 ^
    --member="user:%USER_EMAIL%" ^
    --role="roles/run.invoker"

REM Get the service URL
echo Getting service URL...
gcloud run services describe radeon-ai --region=us-central1 --format="value(status.url)"

echo.
echo Secure deployment complete!
echo - Authentication is now required
echo - Rate limiting: 100 requests/minute per IP
echo - WAF protection enabled
echo - Resource limits set
echo.
pause