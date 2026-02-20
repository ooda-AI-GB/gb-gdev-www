import os
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer(auto_error=False)


def require_api_key(credentials: HTTPAuthorizationCredentials = Security(security)):
    api_key = os.environ.get("GIGABOX_API_KEY", "dev-key")
    if not credentials or credentials.credentials != api_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return credentials.credentials
