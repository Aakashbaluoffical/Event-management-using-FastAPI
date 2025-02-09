from storage.database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String , Float ,DateTime
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = 'user_tbl'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    phone = Column(String(20), index=True)
    email = Column(String, index=True, unique=True)
    role = Column(String, index=True)
    password = Column(String, index=True)
    active = Column(Boolean, index=True)
    
    
    attendees = relationship("Attendee", back_populates="user")
    



class Event(Base):
    __tablename__ = 'event_tbl'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)

    start_time = Column(String, index=True)
    end_time = Column(String, index=True)
    location = Column(String, index=True)
    max_attendees = Column(Integer, index=True)
    status = Column(String,index=True)
    attendees = relationship("Attendee", back_populates="event")



class Attendee(Base):
    __tablename__ = 'attendee_tbl'

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey('event_tbl.id'),index=True)
    user_id = Column(Integer, ForeignKey('user_tbl.id'),index=True)
    check_in_status = Column(Boolean, index=True)
    active = Column(Boolean, index=True)
    created_by_id = Column(Integer, index=True)

    event = relationship("Event", back_populates="attendees")
    user = relationship("User", back_populates="attendees")






