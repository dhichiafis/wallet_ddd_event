class WalletRepository():
    def __init__(self,session):
        self.session=session 
        self.seen=set()

    def add_wallet(self,wallet):
        self.session.add(wallet)
        self.seen.add(wallet)

    def get_all_wallets(self):
        pass 

    def get_wallet_by_id(self):
        pass 

    