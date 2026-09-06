#from domain.models import *
from models.domain import *
class LedgerAccountRepository:
    def __init__(self,session):
        self.session=session
        self.seen=set()

    def create_ledger(self,ledger):
        self.session.add(ledger)
        self.seen.add(ledger)

    def get_all_ledgers(self):
        return self.session.query(LedgerAccount).all()
    
    def get_ledger_by_id(self,id):
        return self.session.query(LedgerAccount).filter(LedgerAccount.id==id).first()

    def get_by_ledger_account_name(self,ledgeraccountname):
        return self.session.query(LedgerAccount).filter(LedgerAccount.ledgeraccountname==ledgeraccountname).first()
    