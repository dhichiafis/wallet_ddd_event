from pydantic import BaseModel

class Command(BaseModel):
    pass 



class RegisterUser(Command):
    username:str 
    password:str 


class LoginUser(Command):
    pass 