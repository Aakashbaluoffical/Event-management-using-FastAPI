import jwt
import bcrypt
from datetime import datetime, timedelta
from configuration.connection import JWT_TOKEN
from fastapi import HTTPException,Depends
from sqlalchemy.orm import Session
from model.model import User


JWT_TOKEN = JWT_TOKEN()

JWT_TOKEN.SECRET_KEY, JWT_TOKEN.ALGORITHM, JWT_TOKEN.ACCESS_TOKEN_EXPIRE_MINUTES

#  Hash password
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

#  Verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

#  Generate JWT Token
def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=JWT_TOKEN.ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    return jwt.encode(data, JWT_TOKEN.SECRET_KEY, algorithm=JWT_TOKEN.ALGORITHM)

#  Authenticate user & generate token
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"user_id": user.id})
    return token





from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# ✅ Extract `user_id` from JWT token
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_TOKEN.SECRET_KEY, algorithms=[JWT_TOKEN.ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
