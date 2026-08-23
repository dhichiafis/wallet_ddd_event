from models.domain import *
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import HTTPException
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

def deposit_to_wallet_handler(wallet,uow):
    with uow as uow:
        try:
            mywallet=uow.walletrepo.get_wallet_by_user_id(user_id=wallet.user_id)
            mywallet.deposit(amount=wallet.amount)
            transaction=Transaction(
            transaction_id=None,
            wallet_id=mywallet.id,
            type='deposit',
            description='deposit to my wallet',
            amount=wallet.amount,
            created_at=datetime.now(ZoneInfo('Africa/Nairobi'))
        )
            uow.transrepo.create_transaction(transaction)
            return {'message':'you have deposited money into your account'}
        except Exception as e:
            return HTTPException(
                detail=str(e),
                status_code=400
            )

def withdraw_from_wallet_handler(wallet,uow):
    with uow as uow:
        try:
            mywallet=uow.walletrepo.get_wallet_by_user_id(user_id=wallet.user_id)
            mywallet.withdraw(amount=wallet.amount)
            transaction=Transaction(
            transaction_id=None,
            wallet_id=mywallet.id,
            type='withdrawal',
            description='withdrawal from my wallet',
            amount=wallet.amount,
            created_at=datetime.now(ZoneInfo('Africa/Nairobi'))
        )
            uow.transrepo.create_transaction(transaction)
            return {'message':'you have withdrawn money from your account'}
        except Exception as e:
            return HTTPException(
                detail=str(e),
                status_code=400
            )
    


def tranfer_to_wallet_handler(wallet,uow):
    with uow as uow:
        pass 

def get_wallet_statements(wallet,uow):
    with uow as uow:
        statements=uow.transrepo.get_
def send_message(wallet,uow):
    print('messag is that your have created your wallet')
    print('this is it with balance',wallet.balance)