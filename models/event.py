from pydantic import BaseModel
from datetime import datetime

class Event(BaseModel):
    pass 


class UserCreated(Event):
    username:str 
    password:str 
    created_at:datetime 
    updated_at:datetime 


class WalletCreated(Event):
    #user_id:int 
    balance:float 
    pin:int 
    created_at:datetime
    #updated_at:datetime 
