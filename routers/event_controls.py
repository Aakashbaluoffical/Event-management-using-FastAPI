from fastapi import APIRouter,Depends,HTTPException
from storage.database import get_db
from cache import cache_set
from sqlalchemy.orm import Session
from schemas .schema import CreateEvent,EventRegistratedResponse,ValidateCheckInCheckOut,EventCancel,EventUpdate

from storage import query_data  






router = APIRouter(tags=["Event Control"])

#====================================================================================
#                     Event Creations 
#====================================================================================

@router.post('/create_event')
def create_event(request : CreateEvent,db:Session = Depends(get_db)):
        # try:
        check_result =query_data.post_event(db,request)
        # except Exception as e:
        #        raise HTTPException(status_code=500, detail=e)  
        if check_result==False:
              raise HTTPException(status_code=404, detail="User not found")  
        return {"data":"Inserted"}#completed
               




@router.get('/view_events')
def view_events(user_id:int = None,db:Session = Depends(get_db)):
        data = cache_set.get_all_registrated_events(db,user_id,True)
        if not data:
              raise HTTPException(status_code=404, detail="Event not found")
        validated_data = [EventRegistratedResponse(**event) for event in data]  # Validate data using Pydantic
        return {"data":validated_data} #completed

# @router.get('/view_booking')
# def view_books(user_id:int = None,db:Session = Depends(get_db)):
#         data = cache_set.get_all_registrated_events(db,user_id,'view_bookings')
#         if not data:
#               raise HTTPException(status_code=404, detail="Event not found")
#         validated_data = [EventRegistratedResponse(**event) for event in data]  # Validate data using Pydantic
#         return {"data":validated_data} 

@router.get('/view_events/{event_id}')
def view_event_by_id(user_id:int = None,event_id:int = None,db:Session = Depends(get_db)):
        data = cache_set.get_all_registrated_events(db,user_id,True)
       
        filtered_data = list(filter(lambda x:x['event_id']==event_id,data))
        
        if not filtered_data:
                raise HTTPException(status_code=404, detail="Event not found")
        
        validated_data = [EventRegistratedResponse(**event) for event in filtered_data]  # Validate data using Pydantic
        return {"data":validated_data} #completed


#====================================================================================
#                     Event modifications 
#====================================================================================

#------- Only Autherized Super user ------------
@router.put('/view_events/{event_id}')
def edits_events(user_id:int,event_id:int,requests:EventUpdate,db:Session = Depends(get_db)):
        data = query_data.update_event(db,requests,user_id,event_id)
        if data['data'] == False:
               raise HTTPException(status_code=404, detail=data['message'])
        return {'data': data['message'] } #completed

@router.put('/view_events/{event_id}/cancel')
def cancel_event_by_id(request:EventCancel,db:Session = Depends(get_db)):
        data = query_data.cancel_the_event(db,request)
        return {'data':'Canceled Event'} #completed

# @router.delete('/view_events/{event_id}/delete')
# def delete_event_by_id(request:EventCancel,db:Session = Depends(get_db)):
#         data = query_data.delete_the_event(db,request)
#         return {'data':'Canceled Event'}


#--------------- Check in & check outs ------------------------
@router.patch('/view_events/{event_id}/{check_status}')
def event_check_in_check_out(request:ValidateCheckInCheckOut,db:Session = Depends(get_db)):
    try:     
        data = query_data.patch_check_in_check_out(db,request)
    except Exception as e:
           print("Error:",e)
    return {"data":"Updated","value":request} #completed





