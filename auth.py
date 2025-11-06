from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from google.oauth2 import id_token
from google.auth.transport import requests
import os

security = HTTPBearer()

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "960026900565-8ntpodmp8ceprohgqgsg9c1g3dchr7q7.apps.googleusercontent.com")

async def verify_google_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify Google OAuth token"""
    try:
        token = credentials.credentials
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
            
        return {
            'email': idinfo['email'],
            'name': idinfo['name'],
            'picture': idinfo.get('picture', ''),
            'user_id': idinfo['sub']
        }
    except ValueError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Authentication failed")

def get_current_user(user_info: dict = Depends(verify_google_token)):
    """Get current authenticated user"""
    return user_info