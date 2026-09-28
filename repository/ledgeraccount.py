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
    

    def get_balance(self, account_name):

        account = (
            self.session.query(LedgerAccount)
            .filter(
                LedgerAccount.ledgeraccountname == account_name
            )
            .one_or_none()
        )

        if account is None:
            raise ValueError(
                f"Ledger account '{account_name}' does not exist"
            )

        total_debit = sum(
            line.debit or 0
            for line in account.ledgeraccount_lines
        )

        total_credit = sum(
            line.credit or 0
            for line in account.ledgeraccount_lines
        )

        if account.type in ("Asset", "Expense"):
            return total_debit - total_credit

        if account.type in ("Liability", "Income"):
            return total_credit - total_debit

        raise ValueError(
            f"Unknown account type: {account.type}"
        )