# CI/CD Pipeline Setup for Google Cloud Run

## Prerequisites
1. Google Cloud Project with billing enabled
2. GitHub repository with admin access

## Setup Steps

### 1. Get Your Project ID
```bash
gcloud config get-value project
```

### 2. Create Service Account
```bash
# Set your project ID (replace with actual ID)
export PROJECT_ID="your-project-id-here"

# Create service account
gcloud iam service-accounts create github-actions \
    --description="Service account for GitHub Actions" \
    --display-name="GitHub Actions" \
    --project=$PROJECT_ID

# Grant necessary roles
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/cloudbuild.builds.editor"

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

### 3. Add GitHub Secrets
Go to your GitHub repository → Settings → Secrets and variables → Actions

Add these secrets:
- **GCP_PROJECT_ID**: Your Google Cloud Project ID (from step 1)
- **GCP_SA_KEY**: Contents of the `key.json` file (entire JSON content)

**Important**: Copy the ENTIRE contents of key.json including the curly braces

### 4. Test Pipeline
```bash
# Make a small change and push
git add .
git commit -m "Test CI/CD pipeline"
git push
```

Check GitHub → Actions tab to see deployment progress

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