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
        fromwallet=uow.walletrepo.get_wallet_by_user_id(user_id=wallet.user_id)
        fromwallet.withdraw(amount=wallet.amount)
        to_wallet = uow.walletrepo.get_wallet_by_id(
            wallet_id=wallet.to_wallet
        )
        to_wallet.deposit(amount=wallet.amount)
        new_tranfer=Transfer(id=None,from_wallet=fromwallet.id,
                             to_wallet=to_wallet.id
                             ,amount=wallet.amount,status='pending',created_at=datetime.now(ZoneInfo('Africa/Nairobi')))
        uow.transferrepo.add_transfer(new_tranfer)

        #  Create source transaction
        withdrawal_transaction = Transaction(
            transaction_id=None,
            wallet_id=fromwallet.id,
            type="transfer_out",
            description=f"Transfer to wallet {to_wallet.id}",
            amount=wallet.amount,
            created_at=datetime.now(
                ZoneInfo("Africa/Nairobi")
            )
        )

        uow.transrepo.create_transaction(
            withdrawal_transaction
        )
        deposit_transaction = Transaction(
            transaction_id=None,
            wallet_id=to_wallet.id,
            type="transfer_in",
            description=f"Transfer from wallet {fromwallet.id}",
            amount=wallet.amount,
            created_at=datetime.now(
                ZoneInfo("Africa/Nairobi")
            )
        )

        uow.transrepo.create_transaction(
            deposit_transaction
        )

        return {'message':f'you have successfully tranfered money to wallet {wallet.to_wallet}'}
def get_wallet_statements(wallet,uow):
    with uow as uow:
        pass 
        #statements=uow.transrepo.get_
def send_message(wallet,uow):
    print('messag is that your have created your wallet')
    print('this is it with balance',wallet.balance)