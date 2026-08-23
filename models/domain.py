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
        if amount<50:
            raise ValueError('you must deposit more than 50 shillings')
        self.balance+=amount


class Transfer():
    def __init__(self):
        self.id 
        self.from_wallet 
        self.to_wallet 
        self.amount 
        self.status 
        self.created_at 
        self.events=[]


class Transaction:
    def __init__(self,transaction_id,wallet_id,type,description,amount,created_at):
        self.transaction_id=transaction_id
        self.wallet_id=wallet_id
        self.type=type 
        self.description=description
        self.amount=amount 
        self.created_at=created_at
        self.events=[]
        self.events.append(TransactionCreated(
            type=self.type,
            description=self.description,
            amount=self.amount,
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
        account_id,
        account_name,
    
        debit,
        credit,
    ):
        self.journalentryline_id = journalentryline_id
        self.account_id = account_id
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
    def __init__(self,ledgeraccountlines_id,membership,description,debit,credit):
        self.ledgeraccountlines_id =ledgeraccountlines_id
        self.membership=membership
        self.description =description
        self.debit =debit
        self.credit =credit