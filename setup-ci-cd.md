# CI/CD Pipeline Setup for Google Cloud Run

## Prerequisites
1. Google Cloud Project with billing enabled
2. GitHub repository with admin access

## Setup Steps

### 1. Create Service Account
```bash
# Create service account
gcloud iam service-accounts create github-actions \
    --description="Service account for GitHub Actions" \
    --display-name="GitHub Actions"

# Get project ID
export PROJECT_ID=$(gcloud config get-value project)

# Grant necessary roles
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/iam.serviceAccountUser"

# Create and download key
gcloud iam service-accounts keys create key.json \
    --iam-account=github-actions@$PROJECT_ID.iam.gserviceaccount.com
```

### 2. Add GitHub Secrets
Go to your GitHub repository → Settings → Secrets and variables → Actions

Add these secrets:
- **GCP_PROJECT_ID**: Your Google Cloud Project ID
- **GCP_SA_KEY**: Contents of the `key.json` file (entire JSON content)

### 3. Enable Required APIs
```bash
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### 4. Test Pipeline
Push code to main branch and check Actions tab in GitHub

## Pipeline Features
- ✅ Automatic deployment on push to main
- ✅ Docker image build and deploy
- ✅ Service URL output
- ✅ Proper authentication
- ✅ Resource configuration (1Gi memory, 1 CPU)

## Manual Deployment (Backup)
```bash
gcloud run deploy radeon-ai --source . --platform managed --region us-central1 --allow-unauthenticated --port 8000 --memory 1Gi --cpu 1 --timeout 300 --max-instances 10
```