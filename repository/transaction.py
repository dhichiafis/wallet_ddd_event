from models.domain import *

class TransactionRepository:
    def __init__(self,session):
        self.session=session
        self.seen=set()

    def create_transaction(self,transaction):
        self.session.add(transaction)
        self.seen.add(transaction)
        #self.session.flush()
        #return transaction

    def get_all_transactions(self):
        return self.session.query(Transaction).all()

    def get_wallet_transactions(self,wallet_id):
        return self.session.query(Transaction).filter(Transaction.wallet_id==wallet_id).all()
    
    def get_transaction_by_id(self,id):
        return self.session.query(Transaction).filter(Transaction.id==id).first()