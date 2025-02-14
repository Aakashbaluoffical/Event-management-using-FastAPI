from model.model import User,Event,Attendee
import json 
from sqlalchemy import and_
from datetime import datetime
from tokenization.auth import hash_password

from sqlalchemy.sql import func



def post_user(db,request):

    hashed_pw = hash_password(request.password)
    
    data = User(
        first_name=request.first_name,
        last_name=request.last_name,
        phone=request.phone,
        email=request.email,
        password=hashed_pw,
        role='user',
        active=True
    )

    db.add(data)
    db.commit()
    db.refresh(data)
    return data.id








def get_all_events(db):
    events = (
        db.query(
            Attendee.id.label("attendee_id"),
            Event.id.label("event_id"),
            Event.name.label("event_name"),
            Event.description,
            Event.start_time,
            Event.end_time,
            Event.location,
            Event.max_attendees,
            User.first_name,
            User.last_name,
            User.phone,
            Event.status
        )
        .filter(Event.max_attendees>0,Attendee.created_by_id!=None)
        .join(Event, Attendee.event_id == Event.id)
        .join(User, Attendee.user_id == User.id)
        .order_by(Event.start_time.desc())
        .enable_eagerloads(False)  # Disable unnecessary eager loading
        .all()
    )
    return [dict(event._mapping) for event in events]  # Correct way to convert Row objects

        
def get_all_users_by_id(db,user_id):
    data = (db.query(
        User.first_name,
        User.last_name ,
        User.phone ,
        User.email
        ).filter(User.id == user_id).first()  
    )
    print("data111111111111",data)
    keys = ["first_name", "last_name", "phone", "email"]
  
    data_dict = dict(zip(keys, data))
    return data_dict
    return json.dumps(data_dict, indent=4)


def check_slots_availabity(db,event_id):
    data = (db.query(
        Event.max_attendees
        ).filter(Event.id == event_id).first()  
    )
    keys=['max_attendees']
    return  dict(zip(keys, data))

def post_registration(db,request,available_slots,user_id):
    slots = available_slots['max_attendees']-1
    
    if int(slots)<0:
        return False
    
    datas = Attendee(user_id = user_id,event_id = request.event_id,active=True)

    db.add(datas)
    db.commit()
    db.refresh(datas)
    print("data posted")

    
    
    db.query(Event).filter_by(id=request.event_id).update({'max_attendees':slots})
    db.commit()
    return True

        
    
def check_already_registrated(db,request,user_id):
    data = (db.query(
        Attendee.user_id,
        Attendee.event_id

        ).filter(Attendee.event_id == request.event_id,Attendee.user_id == user_id,Attendee.active==True).first()  
    )
    if not data:
        return []
    keys=['user_id','event_id']
    return  dict(zip(keys, data))
    



def get_all_registrated_events(db,user_id,owner):

    if owner == True:
        filters = and_(
            Attendee.user_id == user_id,
            Attendee.active == True,
            Attendee.created_by_id == user_id
        )
    elif owner == 'view_bookings':
        print("hererererererererererer")
        filters = and_(
            Attendee.user_id == user_id,
            Attendee.active == True,
            Attendee.created_by_id == None
        )   
    else:
        filters = and_(
            Attendee.user_id == user_id,
            Attendee.active == True
        )

    events = (
        db.query(
            Attendee.id.label("attendee_id"),
            Event.id.label("event_id"),
            Event.name.label("event_name"),
            Attendee.user_id,
            Event.description,
            Event.start_time,
            Event.end_time,
            Event.location,
            Event.max_attendees,
            User.first_name,
            User.last_name,
            User.phone,
            Event.status
        )
        .filter(filters)  # Correctly applying AND conditions
        .join(Event, Attendee.event_id == Event.id)
        .join(User, Attendee.user_id == User.id)
        .order_by(Event.start_time.desc())
        .enable_eagerloads(False)  # Disable unnecessary eager loading
        .all()
    )

    return [dict(event._mapping) for event in events]




def cancel_the_registrated_events(db,update_request,available_slots):
    

    db.query(Attendee).filter(Attendee.user_id==update_request.user_id,Attendee.event_id == update_request.event_id).update({'active':False})
    db.commit()


    slots = available_slots['max_attendees']+1
    db.query(Event).filter_by(id=update_request.event_id).update({'max_attendees':slots})
    db.commit()
    print("updated Slot")

    return db

def post_event(db,request):
    
    datas = Event(name = request.name,
                    description = request.description,
                    start_time = request.start_time,
                    end_time = request.end_time,
                    location = request.location,
                    max_attendees = request.max_attendees,
                    status = request.status
                    )
    

    db.add(datas)
    db.commit()
    db.refresh(datas)
    
    print("datas.iddatas.iddatas.id",datas.id)
    
    
    datas = Attendee(user_id = request.user_id,event_id = datas.id,active=True,created_by_id= request.user_id)
    
    db.add(datas)
    db.commit()
    db.refresh(datas)
    return True


def patch_check_in_check_out(db,update_request):
    print("here")
    checking = (db.query(
        Attendee.created_by_id,
        Attendee.event_id

        ).filter(Attendee.event_id == update_request.event_id,Attendee.created_by_id == update_request.created_id).first()  
    )
    print("checking",checking)
    if not checking:
        return {"data":False,'Error':'created_id not a valid user'}
    

    event = db.query(Attendee).filter(Attendee.user_id == update_request.user_id,Attendee.event_id == update_request.event_id).first()
    print("event",event)
    
    if not event:
        return {"data":False,'Error':'No Records'}

    # Update only the provided fields
    for _, _ in update_request.dict(exclude_unset=True).items():
        print("update_request.check_status:",update_request.check_in_status)
        print("update_request.check_status:",type(update_request.check_in_status))

        setattr(event, 'check_in_status', update_request.check_in_status)

    db.commit()
    db.refresh(event)
    return db



def cancel_the_event(db,request):
    

    db.query(Attendee).filter(Attendee.created_by_id==request.user_id,Attendee.event_id == request.event_id).update({'active':False})
    db.commit()

    db.query(Event).filter(Event.id == request.event_id).update({'status':'Cancelled'})
    db.commit()
   

    return db

# def delete_the_event(db,request):
    

#     # db.query(Attendee).filter(Attendee.created_by_id==request.user_id,Attendee.event_id == request.event_id).update({'active':False})
#     # db.commit()
#     db.query(Attendee).filter(
#         Attendee.created_by_id == request.user_id,
#         Attendee.event_id == request.event_id
#     ).delete(synchronize_session=False)  # Prevents issues with session updates

#     db.commit()
#     return db

def update_event(db,request,user_id,event_id):
    event = db.query(Attendee).filter(Attendee.user_id == user_id,Attendee.event_id == event_id).first()
    if not event:
        return {"data":False,'message':'No Records'}
    update_data = dict(request)

    
    update_data = {key: value for key, value in update_data.items() if value not in [None, ""]}

    if not update_data:
        return {"data":False,"message": "No valid data provided for update"}

    print("================")
    print("request['event_id']",request)
    

    db.query(Event).filter(Event.id == event_id).update(update_data, synchronize_session=False)
    db.commit()
    
    return {"data":True,"message": "Event updated successfully"}



    

from sqlalchemy.sql import text
def update_status(db):  
    updated_rows = (
        db.execute(
            text(
                "UPDATE event_tbl "
                "SET status = 'Completed' "
                "WHERE status != 'Completed' AND status != 'Cancelled' AND TO_TIMESTAMP(end_time, 'YYYY-MM-DD HH24:MI:SS') < :today"
            ),
            {"today": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        )
    )
    db.commit() 




def latet_id(db,table):
    if table == 'user':
        data = db.query(User.id).order_by(User.id.desc()).first()
    elif table=='event':
        data = db.query(Event.id).order_by(Event.id.desc()).first()
    else:
        data = db.query(Attendee.id).order_by(Attendee.id.desc()).first()

      
    data = (data)

    keys=['id']
    return  dict(zip(keys, data))


def get_all_registrated_attendees(db,user_id,event_id):
    events = (
        db.query(
            Attendee.id.label("attendee_id"),
            Event.id.label("event_id"),
            Event.name.label("event_name"),
            Attendee.user_id,
            Event.description,
            Event.start_time,
            Event.end_time,
            Event.location,
            Event.max_attendees,
            User.first_name,
            User.last_name,
            User.phone,
            Event.status
        )
        .filter( Attendee.event_id== event_id,Attendee.created_by_id==None)  # Correctly applying AND conditions
        .join(Event, Attendee.event_id == Event.id)
        .join(User, Attendee.user_id == User.id)
        .order_by(Event.start_time.desc())
        .enable_eagerloads(False)  # Disable unnecessary eager loading
        .all()
    )
    return [dict(event._mapping) for event in events]



def check_the_creater_or_not(db,request,user_id):
    data = (db.query(
        Attendee.user_id,
        Attendee.event_id

        ).filter(Attendee.event_id == request.event_id,Attendee.user_id == user_id,Attendee.created_by_id == user_id,Attendee.active==True).first()  
    )
    if not data:
        return False
    
    return True


