from repository.user import *
from repository.wallet import *
from infrastructure.database import *

class UnitOfWork:
    def __init__(self):
        self.session=None 
        self.userrepo=None 
        self.walletrepo=None 

    def __enter__(self):
        self.session=SessionFactory()
        self.userrepo=UserRepository(session=self.session)
        self.walletrepo=WalletRepository(session=self.session)
        return self 

    def __exit__(self,exc_type, exc_value, traceback):
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def collect_events(self):
        for repo in [self.userrepo,self.walletrepo]:
            for aggregate in repo.seen:
                while aggregate.events:
                    yield aggregate.pop(0)