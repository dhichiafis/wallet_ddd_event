from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import Request
class Event(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


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
    mpesa_receipt:str
    checkout_id:str
    created_at:datetime 


            