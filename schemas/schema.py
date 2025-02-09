from pydantic import BaseModel,Field,validator
from typing import List, Optional
from datetime import datetime
from enum import Enum   


class User(BaseModel):
    first_name: str = Field(..., min_length=1, description="First name is required")
    last_name: str = Field(..., min_length=1, description="Last name is required")
    phone: int = Field(..., description="Phone number is required")
    email: str = Field(..., description="Email is required")
    password: str = Field(..., min_length=6, description="Password is required and must be at least 6 characters")

    @validator("first_name", "last_name", "email", "password")
    def check_not_empty(cls, value):
        if value.strip() == "":
            raise ValueError("Field cannot be empty")
        return value

class EventRegistration(BaseModel):   
    event_id:int

class ValidateCheckInCheckOut(BaseModel):   
    user_id:int
    event_id:int
    created_id:int
    check_in_status:bool

# Define an Enum for allowed status values
class EventStatus(str, Enum):
    scheduled = "Scheduled"
    ongoing = "Ongoing"
    completed = "Completed"
    canceled = "Canceled"

class CreateEvent(BaseModel):
    name: str
    description: str
    start_time: datetime = Field(description="Format: YYYY-MM-DD HH:MM:SS")
    end_time: datetime = Field(description="Format: YYYY-MM-DD HH:MM:SS")
    location:str
    max_attendees:int = Field(gt=0, description="Max attendees must be greater than zero")  # Ensures value > 0
    user_id:int
    status:EventStatus

# class ValidateEventView(BaseModel):
#     event_id:int
#     event_name:str
#     event_start_time:str
#     event_end_time:str
#     event_location:str
#     event_Slots:int
#     conducted_by:str
#     contact_no:int
#     status:str

# class ValidateEventViewResponse(BaseModel):
#     data:list[ValidateEventView]

class EventResponse(BaseModel):
    # attendee_id: int
    event_id: int
    event_name: str
    description: Optional[str]
    start_time: str
    end_time: str
    location: Optional[str]
    max_attendees: Optional[int]
    first_name: str
    last_name: str
    phone: Optional[str]
    status: str

    class Config:
        from_attributes = True  # Allows SQLAlchemy object conversion


class EventRegistratedResponse(BaseModel):
    # attendee_id: int
    event_id: int
    user_id: int

    event_name: str
    description: Optional[str]
    start_time: str
    end_time: str
    location: Optional[str]
    max_attendees: Optional[int]
    first_name: str
    last_name: str
    phone: Optional[str]
    status: str

    class Config:
        from_attributes = True  # Allows SQLAlchemy object conversion

class EventCancel(BaseModel):
    user_id: int 
    event_id: int




class EventUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    max_attendees: Optional[int] = Field(None, gt=0)  # Must be > 0
    status: Optional[str] = Field(None, pattern="^(Scheduled|Ongoing|Completed|Canceled)$")




    class Config:
        from_attributes = True  # Enable ORM Mode



