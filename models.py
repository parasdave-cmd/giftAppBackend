from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Time
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.ext.declarative import declarative_base, as_declarative
import datetime
from pytz import timezone
import pytz

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)

    gifts = relationship("Gifts", back_populates="owner")

class Gifts(Base): 
    __tablename__ = "gifts"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    description = Column(String)
    owner_name = Column(String, ForeignKey("users.username"))
    owner = relationship("Users", back_populates="gifts")
    
class Audits(Base):
    __tablename__ = "audits"
    
    id = Column(Integer, primary_key=True)
    action = Column(String, index=True)
    object = Column(String, index=True)
    time = Column(String, default=lambda: datetime.datetime.now(timezone("America/Los_Angeles")).strftime("%m/%d/%Y, %H:%M:%S"))