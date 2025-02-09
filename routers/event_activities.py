from fastapi import APIRouter, Depends,HTTPException,Request
from sqlalchemy.orm import Session
from storage.database import get_db
from schemas.schema import EventRegistration,EventResponse,EventRegistratedResponse,EventCancel
from cache import cache_set
import json
from fastapi.encoders import jsonable_encoder
from storage import query_data 
from typing import List




router = APIRouter(tags=["Event Activities"])


def check_and_update_status(db):
        try:
                query_data.update_status(db)
        except Exception as e:
               print("ERRRRRRER:",e)
               raise HTTPException(status_code=404, detail="Event not found")
              




#====================================================================================
#                     Event activities 
#====================================================================================
@router.get('/view_all_events',response_model=List[EventResponse]) 
def view_all_events(db:Session = Depends(get_db)):
        data = cache_set.get_all_events(db)
        if not data:
              raise HTTPException(status_code=404, detail="Event not found")
        validated_data = [EventResponse(**event) for event in data]  # Validate data using Pydantic
        return validated_data    # completed
        
    

@router.get('/view_event/{event_id}',response_model=List[EventResponse])
def view_event_by_id(event_id: int, db: Session = Depends(get_db)):
    data = cache_set.get_all_events(db)

    filtered_data = list(filter(lambda x:x['event_id']==event_id,data))
    if not filtered_data:
            raise HTTPException(status_code=404, detail="Event not found")
    validated_data = [EventResponse(**event) for event in filtered_data]  # Validate data using Pydantic
    return validated_data  # completed



#====================================================================================
#                     Event registrations 
#====================================================================================

@router.post('/viewall/register')
async def register_event(request: EventRegistration,db:Session = Depends(get_db)):
        
        check_result =query_data.check_already_registrated(db,request)
        if check_result:
              raise HTTPException(status_code=404, detail="Already Registrated")

        available_slots = query_data.check_slots_availabity(db,request.event_id)
       
        if available_slots['max_attendees'] == 0:
               raise  HTTPException(status_code=404, detail="Sold Out")  
               
        user_details = query_data.get_all_users_by_id(db,request.user_id)
        if not user_details:
              raise HTTPException(status_code=404, detail="User not found")  
        
         
        try:
            result = query_data.post_registration(db,request,available_slots)
            if result == False:
                raise HTTPException(status_code=404, detail="Sold Out") 
        except Exception as e:
               print("Error: ",e)
        
        return {'data':{'name': "Registration Completed!" }} #completed


@router.get('/viewall/registrated')
def viewall_registrated(user_id:int = None,db:Session = Depends(get_db)):
        data = cache_set.get_all_registrated_events(db,user_id,False)
        if not data:
              raise HTTPException(status_code=404, detail="Event not found")
        validated_data = [EventRegistratedResponse(**event) for event in data]  # Validate data using Pydantic
        return {"data":validated_data} #completed
        

@router.get('/viewall/registrated/{event_id}')
def viewall_registrated_by_id(user_id:int = None,event_id:int = None,db:Session = Depends(get_db)):
        data = cache_set.get_all_registrated_events(db,user_id,False)
       
        filtered_data = list(filter(lambda x:x['event_id']==event_id,data))
        
        if not filtered_data:
                raise HTTPException(status_code=404, detail="Event not found")
        
        validated_data = [EventRegistratedResponse(**event) for event in filtered_data]  # Validate data using Pydantic
        return {"data":validated_data} #completed


@router.patch('/viewall/registrated/{event_id}/cancel')
def cancel_registration_by_id(update_request:EventCancel,db:Session = Depends(get_db)):
        available_slots = query_data.check_slots_availabity(db,update_request.event_id)
        try:
                data = query_data.cancel_the_registrated_events(db, update_request,available_slots)
        
        except Exception as e:
                print("Error:", str(e))  # Log the actual error
                raise HTTPException(status_code=500, detail="Query Issue")

        if data is False:
                raise HTTPException(status_code=404, detail="Event not found")

        return {"data": "Updated!"}#completed




