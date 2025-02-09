from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from storage.database import get_db
from schemas.schema import User
from storage import query_data
from sqlalchemy.exc import IntegrityError

from tokenization.auth  import hash_password, authenticate_user
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(tags=['Logins'])

@router.post("/signup")
def create_new_account(request: User, db: Session = Depends(get_db)):
    try:
        data = query_data.post_user(db,request)
        print("data=================",data)
    except IntegrityError as e:  # Handle unique constraint violation
        db.rollback()  # Rollback the transaction to keep DB consistent
        raise HTTPException(status_code=400, detail="Email already exists. Please use a different email.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
    return{"data":"User Created","User_id":data}

@router.post("/signin")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    token = authenticate_user(db, form_data.username, form_data.password)
    return {"access_token": token, "token_type": "bearer"}