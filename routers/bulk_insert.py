from fastapi import APIRouter,Depends,HTTPException ,UploadFile,File
from fastapi.responses import JSONResponse
from model.model import User,Event, Attendee
from storage.database import get_db
from typing import Annotated
from sqlalchemy.orm import Session
import pandas as pd
import io
from storage import query_data

router = APIRouter(tags=['Bulk data insertion'])





@router.post("/bulk_insertion")
def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = file.file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
        
        users = []
        events = []
        attendees = []
        try:
            df['start_time'] = pd.to_datetime(df['start_time'], format= '%d/%m/%Y %H:%M:%S').dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            pass
        try:
            df['end_time'] = pd.to_datetime(df['end_time'], format= '%d/%m/%Y %H:%M:%S').dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            pass
        user_id = query_data.latet_id(db,'user')
        event_id = query_data.latet_id(db,'event')
        attendee_id = query_data.latet_id(db,'attendee')

        user_id = int(user_id['id'])+1
        event_id = int(event_id['id'])+1
        attendee_id = int(attendee_id['id'])+1

        # event_mapping = {row["event_name"]: idx for idx, row in zip(range(event_id, event_id + len(df)), df.itertuples())}
        event_mapping = {row.event_name: idx for idx, row in zip(range(event_id, event_id + len(df)), df.itertuples(index=False))}

        for _, row in df.iterrows():
            user_id += 1
            users.append(User(
                id=user_id,
                first_name=row["first_name"],
                last_name=row["last_name"],
                phone=row["phone"],
                email=row["email"],
                role=row["role"],
                password=row["password"],
                active=row["active"]
            ))

            event_id += 1
            events.append(Event(
                id=event_id,
                name=row["event_name"],
                description=row["event_description"],
                start_time=row["start_time"],
                end_time=row["end_time"],
                location=row["location"],
                max_attendees=row["max_attendees"],
                status=row["status"]
            ))

            attendee_id += 1
            attendees.append(Attendee(
                id=attendee_id,
                event_id=event_mapping.get(row["event_name"]),  # Ensure event exists
                user_id=user_id,  # Use the latest user_id
                active=row["attendee_active"],
                created_by_id=row["created_by_id"]
            ))

        db.add_all(users)
        db.add_all(events)
        db.add_all(attendees)
        db.commit()
        
        return JSONResponse(content={"message": "Data inserted successfully"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
  
