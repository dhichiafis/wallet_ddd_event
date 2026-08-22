from models.event import *
class User:
    def __init__(self,id,username,password,is_active,created_at,updated_at):
        self.id =id
        self.username =username
        self.password =password
        self.is_active =is_active
        self.created_at=created_at
        self.updated_at=updated_at
        self.events=[]
        self.events.append(
            UserCreated(
                username=self.username,
                password=self.password,
                created_at=self.created_at,
                updated_at=self.updated_at))


class Wallet:
    def __init__(self,id,balance,pin,created_at):
        self.id 
        self.balance 
        self.pin 
        self.created_at 
        self.events=[]
        self.events.append(WalletCreated(
            balance=self.balance,
            pin=self.pin ,
            created_at=self.created_at,
            updated_at=self.updated_at
        ))


    def set_pin(self):
        pass 

    
    def transfer(self):
        pass 

    def withdraw(self):
        pass 

    def deposit(self):
        pass 

