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
    def __init__(self,id,user_id,balance,pin,created_at):
        self.id =id 
        self.user_id=user_id
        self.balance =balance
        self.pin =pin  
        self.created_at =created_at
        self.events=[]
        self.events.append(WalletCreated(
            balance=self.balance,
            pin=self.pin ,
            created_at=self.created_at,
           # updated_at=self.updated_at
        ))


    def reset_pin(self):
        #if secret answer matches the asnwer
        pass 

    
    '''
    is htis a method of the wallet aggregate 
    def transfer
    '''

    def withdraw(self,amount):
         
        if self.balance<amount:
            raise ValueError('you have insufficient balance')
        self.balance-=amount 
    def deposit(self,amount):
        self.balance+=amount


class Transfer():
    def __init__(self):
        self.id 
        self.from_wallet 
        self.to_wallet 
        self.amount 
        self.status 
        self.created_at 
        
