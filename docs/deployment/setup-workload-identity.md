# Setup Workload Identity Federation (No Secrets!)

## 1. Create Workload Identity Pool
```bash
gcloud iam workload-identity-pools create "github-pool" \
  --project="radeon-ai-kb-2024" \
  --location="global" \
  --display-name="GitHub Actions Pool"
```

## 2. Create Workload Identity Provider
```bash
gcloud iam workload-identity-pools providers create-oidc "github-provider" \
  --project="radeon-ai-kb-2024" \
  --location="global" \
  --workload-identity-pool="github-pool" \
  --display-name="GitHub Provider" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository" \
  --issuer-uri="https://token.actions.githubusercontent.com"
```

## 3. Get Provider Resource Name
```bash
gcloud iam workload-identity-pools providers describe "github-provider" \
  --project="radeon-ai-kb-2024" \
  --location="global" \
  --workload-identity-pool="github-pool" \
  --format="value(name)"
```

## 4. Allow GitHub to Impersonate Service Account
```bash
gcloud iam service-accounts add-iam-policy-binding \
  "github-actions@radeon-ai-kb-2024.iam.gserviceaccount.com" \
  --project="radeon-ai-kb-2024" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/github-pool/attribute.repository/GeorgeRCAdamJohnson/radeon_SML"
```

## 5. Get Project Number
```bash
gcloud projects describe radeon-ai-kb-2024 --format="value(projectNumber)"
```

## 6. Add GitHub Secrets
Only need these 2 secrets (no JSON keys!):

- **WIF_PROVIDER**: `projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/github-pool/providers/github-provider`
- **WIF_SERVICE_ACCOUNT**: `github-actions@radeon-ai-kb-2024.iam.gserviceaccount.com`

## Benefits
✅ No service account keys to manage  
✅ More secure (temporary tokens)  
✅ Automatic rotation  
✅ GitHub-native authentication