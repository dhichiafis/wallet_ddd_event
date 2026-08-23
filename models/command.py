from pydantic import BaseModel

class Command(BaseModel):
    pass 



class RegisterUser(Command):
    username:str 
    password:str 


class LoginUser(Command):
    pass 



class CreateWalletRequest(Command):
    balance:float 
    pin:int 

class CreateWallet(Command):
     #this is crucial since our message bus will be recieving the same interface of commands 
     user_id:int 
     balance:float 
     pin:int 