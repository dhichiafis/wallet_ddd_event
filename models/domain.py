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
        self.phonenumber=phonenumber
        self.is_verified=False
        self.created_at=created_at
        self.events=[]
        self.events.append()

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
            self.phonenumber and self.phonenumber.strip(),
            ])


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
        if amount<50:
            raise ValueError('you must deposit more than 50 shillings')
        self.balance+=amount


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