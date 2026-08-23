#from domain.models import *
from models.domain import *
class LedgerAccountRepository:
    def __init__(self,session):
        self.session=session
        self.seen=set()

    def create_journal_entry(self,ledger):
        self.session.add(ledger)
        self.seen.add(ledger)

    def get_all_journal_entries(self):
        return self.session.query(LedgerAccount).all()
    
    def get_journal_entry_by_id(self,id):
        return self.session.query(LedgerAccount).filter(LedgerAccount.id==id).first()