# main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth import create_token, verify_token

app = FastAPI()
security = HTTPBearer()

@app.post("/login")
def login():
    token = create_token("admin")
    return {"token": token}

@app.get("/dashboard")
def dashboard(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=403, detail="Invalid token")
    return {"message": f"Welcome {user['sub']}"}
