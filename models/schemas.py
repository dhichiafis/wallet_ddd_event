from pydantic import BaseModel,EmailStr
from datetime import datetime
class TopicCreate(BaseModel):
    title:str 
    description:str 


class UserCreate(BaseModel):
    username:str  
    password:str 


class UserBase(BaseModel):
    username:str 
    created_at:datetime

class PasswordReset(BaseModel):
    username:str 
    password:str 


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str  