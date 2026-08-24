
from models.domain import *
class TransferRepository():
    def __init__(self,session):
        self.session=session 
        self.seen=set()

    def add_transfer(self,transfer):
        self.session.add(transfer)
        self.seen.add(transfer)

    def get_all_transfers(self):
        return self.session.query(Transfer).all()

    def get_transfer_by_id(self):
        return self.session.query(Transfer).filter(Transfer.id==id).first()
