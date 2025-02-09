from fastapi import APIRouter,Depends,HTTPException ,UploadFile,File
from storage.database import get_db
from typing import Annotated
from sqlalchemy.orm import Session
import pandas as pd
import io


router = APIRouter(tags=['Bulk data insertion'])





@router.post("/bulk_insertion")
async def bulk_insertion(file: UploadFile = File(...),db: Session = Depends(get_db)):
    contents = await file.read()
    contents_str = contents.decode()
    file_like_object = io.StringIO(contents_str)
    try:
        df = pd.read_csv(file_like_object)
    except:
        raise HTTPException(detail='Unsupported file',status_code=415)  
    
    
    df['start_date'] = pd.to_datetime(df['start_date'], format= '%d/%m/%Y %H:%M:%S').dt.strftime('%Y-%m-%d %H:%M:%S')
    df['end_date'] = pd.to_datetime(df['end_date'], format= '%d/%m/%Y %H:%M:%S').dt.strftime('%Y-%m-%d %H:%M:%S')


    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    df3 = pd.DataFrame()


    df1['first_name'] = df['first_name']
    df1['last_name'] = df['last_name']
    df1['phone'] = df['phone']
    df1['email'] = df['email']
    df1['role'] = df['role']
    df1['active'] = df['active']

    df2['description'] = df['description']
    df2['start_time'] = df['start_time']
    df2['end_time'] = df['end_time']
    df2['location'] = df['location']
    df2['max_attendees'] = df['max_attendees']

    df3['event_id'] = df['event_id']
    df3['user_id'] = df['user_id']
    df3['check_in_status'] = df['check_in_status']


    if df1.empty:
        raise HTTPException("No data",status_code=204)
    
    
  
