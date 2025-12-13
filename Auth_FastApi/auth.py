# auth.py
from jose import jwt
from datetime import datetime, timedelta, timezone

SECRET = "secret"       # Secret key
ALGORITHM = "HS256"     # Algo for signature

# Token banane ka function
def create_token(username: str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    data = {"sub": username, "exp": expire}
    token = jwt.encode(data, SECRET, algorithm=ALGORITHM)
    return token

# Token check karne ka function
def verify_token(token: str):
    try:
        decoded = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return decoded
    except:
        return None
