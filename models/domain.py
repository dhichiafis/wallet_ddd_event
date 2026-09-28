from models.event import *

import re


class PhoneNumber:
    def __init__(self, value: str):
        self.value = self.normalize(value)
        self.validate()

    @staticmethod
    def normalize(value: str) -> str:
        if not value:
            raise ValueError("Phone number is required")

        value = value.strip().replace(" ", "")

        if value.startswith("+254"):
            value = value[1:]

        elif value.startswith("0"):
            value = "254" + value[1:]

        elif not value.startswith("254"):
            raise ValueError("Invalid Kenyan phone number")

        return value

    def validate(self):
        if not re.fullmatch(r"254[17]\d{8}", self.value):
            raise ValueError("Invalid Kenyan phone number")

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, PhoneNumber):
            return self.value == other.value

        return False
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


'''
we are interested in the profile for doing the following one when the profile is created we tehn prompt for pin okay

'''
"""
the profile must have values otherwise we throught out errors to the user similarly we will be validating twice in the frontend as well 

"""
class Profile:
    def __init__(self,id,user_id,firstname,lastname,phonenumber,created_at):
        self.id =id 
        self.user_id=user_id
        self.firstname=firstname 
        self.lastname=lastname 
        self.phonenumber=PhoneNumber(phonenumber).value
        self.is_verified=False
        self.created_at=created_at
        self.events=[]
        #self.events.append()

    def validate(self):
        if self.firstname is None:
            raise ValueError('firstname cannot be empty')
        if self.lastname is None:
            raise ValueError('firstname cannot be empty')
        if self.phonenumber is None:
            raise ValueError('phone number must be provided') 
        
    def is_complete(self):
        return all([
            self.firstname and self.firstname.strip(),
            self.lastname and self.lastname.strip(),
            self.phonenumber,
            ])


class Wallet:
    def __init__(self,id,user_id,balance,pin,created_at):
        self.id =id 
        self.user_id=user_id

        self.balance =balance
        self.pin =pin  
        self.created_at =created_at
        self.events=[]
        self.goals=[]
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
        if amount<50:
            raise ValueError('you must deposit more than 50 shillings')
        self.balance+=amount

    def create_goal(self,goal):
        self.goals.append(goal)

class Goal:
    def __init__(self,goal_id,wallet_id,goal_name,target_amount,target_duration,purpose,created_at,updated_at):
        self.goal_id=goal_id
        self.wallet_id=wallet_id
        self.goal_name=goal_name
        self.target_amount=target_amount 
        self.target_duration=target_duration
        self.purpose=purpose
        self.created_at=created_at
        self.updated_at=updated_at
        self.events=[]
        self.contributions=[]

    def add_daily_contributions(self,contribution):
        if contribution.contribution_amount <= 0:
            raise ValueError(
                "Contribution must be greater than zero"
            )

        if self.current_amount + contribution.contribution_amount > self.target_amount:
            raise ValueError(
                "Contribution would exceed the goal target"
            )

        self.contributions.append(contribution)
        


class GoalContributions:
    def __init__(self):
        self.goal_contribution_id 
        self.goal_id 
        self.contribution_amount 
        self.contribution_date 
        self.events=[]
        

class Transfer():
    def __init__(self,id,from_wallet,to_wallet,amount,
                status,created_at):
        self.id =id
        self.from_wallet =from_wallet
        self.to_wallet =to_wallet
        self.amount =amount
        self.status =status
        self.created_at =created_at
        self.events=[]
        '''
        self.events.append(
                    CreateTransfer(
                        from_wallet=self.from_wallet,
                        to_wallet=self.to_wallet,
                        amount=self.amount,
                        status=self.status,
                        created_at=self.created_at
                    )
                )
        
        '''
class Transaction:
    def __init__(self,
    transaction_id,wallet_id,type,description,amount,status
    ,mpesa_reciept,checkout_id,created_at):
        self.transaction_id=transaction_id
        self.wallet_id=wallet_id
        self.type=type 
        self.description=description
        self.amount=amount 
        self.status=status
        self.mpesa_receipt=mpesa_reciept #these two fields are useful for audit
        self.checkout_id=checkout_id #now the transaction is asynchronous the user has not enter pin so we have to wait 
        self.created_at=created_at
        self.events=[]
        self.events.append(TransactionCreated(
            type=self.type,
            description=self.description,
            amount=self.amount,
            mpesa_receipt=self.mpesa_receipt,
            checkout_id=self.checkout_id,
            created_at=self.created_at
        ))

class JournalEntry:
    def __init__(self,journalentry_id,description,created_at):
        self.journalentry_id=journalentry_id
    
        self.description=description
        self.created_at=created_at
        self.lines=[] 
        self.events=[]

    def valid_entry(self):
        return self.total_credits()==self.total_debits()
    
    def add_lines(self,line):
        self.lines.append(line)
    def total_debits(self):
        return sum(line.debit for line in self.lines)
    
    def total_credits(self):
        return sum(line.credit for line in self.lines)

class JournalEntryLine:
    def __init__(
        self,
        journalentryline_id,
        wallet_id,
        account_name,
    
        debit,
        credit,
    ):
        self.journalentryline_id = journalentryline_id
        self.wallet_id = wallet_id
        self.account_name = account_name
        self.debit = debit
        self.credit = credit


class LedgerAccount:
    def __init__(self,ledgeracc_id,ledgeraccountname,type,created_at):
        self.ledgeracc_id=ledgeracc_id
        self.ledgeraccountname =ledgeraccountname

        self.type =type
        
        self.created_at=created_at
        self.ledgeraccount_lines=[]

    def get_balance(self):
        return "the balance is "
    
    def post_to_ledger(self,accountline):
        self.ledgeraccount_lines.append(accountline)

class LedgerAccountLines:
    def __init__(self,ledgeraccountlines_id,wallet_id,description,debit,credit):
        self.ledgeraccountlines_id =ledgeraccountlines_id
        self.wallet_id=wallet_id
        self.description =description
        self.debit =debit
        self.credit =credit