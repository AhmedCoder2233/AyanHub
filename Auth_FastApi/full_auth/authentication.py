from jose import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

SECRET = "supersecret"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users_db = {}  # username: hashed_password

def create_token(username: str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=2)
    data = {"sub": username, "exp": expire}
    return jwt.encode(data, SECRET, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        decoded = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return decoded
    except:
        return None

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)
