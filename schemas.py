from typing import List, Union

from pydantic import BaseModel


class GiftBase(BaseModel):
    name: str
    description: Union[str, None] = None


class GiftCreate(GiftBase):
    pass


class Gift(GiftBase):
    id: int
    owner_name: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str

class UserUpdate(BaseModel):
    is_admin: bool

class UserCreate(UserBase):
    password: str
    is_admin: bool


class User(UserBase):
    id: int
    gifts: List[Gift] = []
    is_admin: bool

    class Config:
        orm_mode = True

class AuditBase(BaseModel):
    action: str
    object: str
    
class AuditCreate(AuditBase):
    pass
    
class Audit(AuditBase):
    id: int
    time: str
    
    class Config:
        orm_mode = True
        #arbitrary_types_allowed = True
