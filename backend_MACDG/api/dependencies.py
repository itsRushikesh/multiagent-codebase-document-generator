from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from backend_MACDG.utils.jwt_utils import decode_access_token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        return {"id": payload['user_id'], "role": payload['role']}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")

def require_admin(user=Depends(get_current_user)):
    if user['role'] != 'Admin':
        raise HTTPException(status_code=403, detail="Admin access required.")
    return user
