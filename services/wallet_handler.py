from models.domain import *
from datetime import datetime
from zoneinfo import ZoneInfo


def create_wallet_handler(wallet,uow):
    with uow as uow:
        new_wallet=Wallet(
            id=None,
            user_id=wallet.user_id,
            balance=wallet.balance,
            pin=wallet.pin,
            created_at=datetime.now(ZoneInfo('Africa/Nairobi'))

        )
        uow.walletrepo.add_wallet(new_wallet)
        return {'message':"wallet created successfully"}


def send_message(wallet,uow):
    print('messag is that your have created your wallet')
    print('this is it with balance',wallet.balance)