from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from storage.database import get_db
from schemas.schema import User
from storage import query_data
from sqlalchemy.exc import IntegrityError


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
def login(user: User, db: Session = Depends(get_db)):
    # Implement user login logic here
    return {'data':{'message': "Logged in successfully" }}