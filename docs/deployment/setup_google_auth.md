# Google Authentication Setup

## 1. Create Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project: `radeon-ai-kb-2024`
3. Navigate to **APIs & Services > Credentials**
4. Click **Create Credentials > OAuth 2.0 Client IDs**
5. Configure:
   - Application type: **Web application**
   - Name: `Radeon AI Web Client`
   - Authorized JavaScript origins: 
     - `http://localhost:8080`
     - `https://YOUR_CLOUD_RUN_URL`
   - Authorized redirect URIs:
     - `http://localhost:8080`
     - `https://YOUR_CLOUD_RUN_URL`

## 2. Update Configuration

Replace `YOUR_GOOGLE_CLIENT_ID` in these files:
- `static/login.html` (2 places)
- Set environment variable: `GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com`

## 3. Deploy with Environment Variable

```bash
gcloud run deploy radeon-ai \
  --source . \
  --platform managed \
  --region us-central1 \
  --no-allow-unauthenticated \
  --set-env-vars GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
```

## 4. Test Authentication

1. Visit your Cloud Run URL
2. You'll be redirected to login page
3. Sign in with Google
4. Access the chat interface

## Security Features Added

- ✅ Google OAuth authentication
- ✅ JWT token validation
- ✅ Protected API endpoints
- ✅ User session management
- ✅ Automatic logout on token expiry