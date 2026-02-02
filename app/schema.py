from dataclasses import Field
from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime

class Postbase(BaseModel):
    title: str
    content: str
    rating: Optional[int] = None
    published: bool = True

class createpost(Postbase):
    pass

class Userresponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime.datetime
    class Config:
        orm_mode = True

class userresponsemail(BaseModel):
    email: EmailStr
    class Config:
        orm_mode = True

class Postresponse(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int
    owner: userresponsemail
    published: bool = True
    class Config:
        orm_mode = True

class Postwithvote(BaseModel):
    Post:Postresponse
    votes:int
    class Config:
        orm_mode = True

class Userbase(BaseModel):
    email: EmailStr
    password: str

class Userlogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None    

class Vote(BaseModel):
    post_id: int
    dir: int 