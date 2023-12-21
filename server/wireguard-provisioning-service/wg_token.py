# wireguard-provisioning-service/wg_token.py

from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer
from database import is_token_valid, add_token
import secrets

security = HTTPBearer()

def validate_token(http_auth: HTTPBearer = Security(security)):
    token = http_auth.credentials
    if not is_token_valid(token):
        raise HTTPException(status_code=401, detail="Invalid token")

def generate_token():
    token = secrets.token_hex(16)
    add_token(token)
    return token
