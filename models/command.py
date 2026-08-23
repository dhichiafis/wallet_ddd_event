from pydantic import BaseModel
from decimal import Decimal
class Command(BaseModel):
    pass 


"""
for the amount well be using decimal which is stored in the database as numeric otherwise using a float gives a mismatch
"""
class RegisterUser(Command):
    username:str 
    password:str 


class LoginUser(Command):
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


class GetStatement(Command):
    wallet_id:int 