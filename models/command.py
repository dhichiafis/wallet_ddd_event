from datetime import datetime
from pydantic import BaseModel,ConfigDict
from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import Request 
class Command(BaseModel):
    #this allow us to pass python objects that are not necessarily models
    model_config = ConfigDict(arbitrary_types_allowed=True)


"""
for the amount well be using decimal which is stored in the database as numeric otherwise using a float gives a mismatch
"""
class RegisterUser(Command):
    username:str 
    password:str 


class LoginUser(Command):
    pass 


class GetAllUser(Command):
    pass 
class CreateWalletRequest(Command):
    balance:Decimal 
    pin:int 

class CreateWallet(Command):
     #this is crucial since our message bus will be recieving the same interface of commands 
     user_id:int 
     balance:Decimal 
     pin:int 


class CreateTransaction(Command):
    type:str 
    description:str 
    amount:Decimal 

class DepositToWalletRequest(Command):
    amount:Decimal 

class DepositToWallet(Command):
    amount:Decimal 
    user_id:int 

class WithdrawFromWalletRequest(Command):
    amount:Decimal 

class WithdrawFromWallet(Command):
    amount:Decimal 
    user_id:int 

 
class CreateProfileRequest(Command):
     
    firstname:str 
    lastname:str 
    phonenumber:str 


class CreateProfile(CreateProfileRequest):
    user_id:int
    
class GetStatement(Command):
    wallet_id:int 

class CreateTranferRequest(Command):
    #from_wallet:int 
    to_wallet:int 
    amount:Decimal
    #status:str 
    #created_at:datetime 


class CreateTransfer(Command):
    user_id:int
    #from_wallet:int
    to_wallet:int 
    amount:Decimal
    #status:str
    #created_at:datetime 

class TransactionPaymentCallback(Command):
    db:Session 
    reqs:Request 

#this crashes the app because session and request are not pydantic models so a better correction
class MpesaStkCallBack(Command):
    db:Session
    reqs:Request



class CompleteRegistration(Command):
    user_id: int
    firstname: str
    lastname: str
    phonenumber: str
    pin: int