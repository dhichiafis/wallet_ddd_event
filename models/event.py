from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
class Event(BaseModel):
    pass 


class UserCreated(Event):
    username:str 
    password:str 
    created_at:datetime 
    updated_at:datetime 


class WalletCreated(Event):
    #user_id:int 
    balance:Decimal
    pin:int 
    created_at:datetime
    #updated_at:datetime 

class TransactionCreated(Event):
    type:str 
    description:str 
    amount:Decimal
    created_at:datetime 
            