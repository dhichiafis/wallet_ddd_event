from models.domain import *
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import HTTPException
from services.payments import *


from pwdlib import PasswordHash
password_hash = PasswordHash.recommended()
# since any transaction done in the wallet pin must be hashed instead of storing numbers 

def get_pin_hash(pin):
    return password_hash.hash(pin)
    
def verify_pin(pin,hashed_pin):
    return password_hash.verify(pin,hashed_pin)


def complete_registration_handler(command, uow):

    with uow as uow:

        user = uow.userrepo.get_user_by_id(command.user_id)

        if user is None:
            raise ValueError("User not found")

        profile = Profile(
            id=None,
            user_id=user.id,
            firstname=command.firstname,
            lastname=command.lastname,
            phonenumber=command.phonenumber,
            created_at=datetime.now(ZoneInfo("Africa/Nairobi"))
        )

        profile.validate()

        if not profile.is_complete():
            raise ValueError("Profile is incomplete")

        hashed_pin = get_pin_hash(command.pin)

        newwallet = Wallet(
            id=None,
            user_id=user.id,
            balance=Decimal("0"),
            pin=hashed_pin,
            created_at=datetime.now(ZoneInfo("Africa/Nairobi"))
        )

        uow.profilerepo.add(profile)
        uow.walletrepo.add_wallet(newwallet)

        user.is_active = True

        return {
            "message": "Account setup completed"
        }


def create_wallet_handler(wallet,uow):
    with uow as uow:
        pin=get_pin_hash(wallet.pin)
        new_wallet=Wallet(
            id=None,
            user_id=wallet.user_id,
            balance=0,
            pin=pin,
            created_at=datetime.now(ZoneInfo('Africa/Nairobi'))
        )
        uow.walletrepo.add_wallet(new_wallet)
        return {'message':"wallet created successfully"}

#this method has to invoke the stk push 
def deposit_to_wallet_handler(wallet,uow):
    with uow as uow:
        try:
            mywallet=uow.walletrepo.get_wallet_by_user_id(user_id=wallet.user_id)
            mywallet.deposit(amount=wallet.amount)
            transaction=Transaction(
            transaction_id=None,
            wallet_id=mywallet.id,
            type='deposit',
            description=f'deposit to my wallet {mywallet.id}',
            amount=wallet.amount,
            created_at=datetime.now(ZoneInfo('Africa/Nairobi'))
        )
            uow.transrepo.create_transaction(transaction)
            cash_account=uow.ledgeraccrepo.get_by_ledger_account_name('Cash Account')
            if cash_account is None:
                raise ValueError(
                    "Cash Account does not exist"
                )
            wallet_withdrawable_account=uow.ledgeraccrepo.get_by_ledger_account_name('Wallet Withdrawable Account')
                        

            if wallet_withdrawable_account is None:
                raise ValueError(
                    "Wallet Liability Account does not exist"
                )
            journal_entry = JournalEntry(
                journalentry_id=None,

                description=(
                    f"Deposit of {wallet.amount} "
                    f"to wallet {mywallet.id}"
                ),

                created_at=datetime.now(
                    ZoneInfo("Africa/Nairobi")
                )
            )
            cash_line = JournalEntryLine(

                journalentryline_id=None,

                # We carry the wallet ID from the transaction.
                wallet_id=transaction.wallet_id,

                account_name=cash_account.ledgeraccountname,

                debit=wallet.amount,

                credit=0
            )
            wallet_line = JournalEntryLine(

                journalentryline_id=None,

                wallet_id=transaction.wallet_id,

                account_name=wallet_withdrawable_account.ledgeraccountname,

                debit=0,

                credit=wallet.amount
            )
            journal_entry.add_lines(
                cash_line
            )

            journal_entry.add_lines(
                wallet_line
            )
            if not journal_entry.valid_entry():

                raise ValueError(
                    "Journal entry is not balanced"
                )
            cash_ledger_line = LedgerAccountLines(

                ledgeraccountlines_id=None,

                wallet_id=transaction.wallet_id,

                description=(
                    f"Deposit to wallet "
                    f"{transaction.wallet_id}"
                ),

                debit=wallet.amount,

                credit=0
            )
            wallet_ledger_line = LedgerAccountLines(

                ledgeraccountlines_id=None,

                wallet_id=transaction.wallet_id,

                description=(
                    f"Deposit to wallet "
                    f"{transaction.wallet_id}"
                ),

                debit=0,

                credit=wallet.amount
            )
            cash_account.post_to_ledger(
                cash_ledger_line
            )
            wallet_withdrawable_account.post_to_ledger(
                wallet_ledger_line
            )
            uow.ledgeraccountrepo.create_ledger(
                cash_account
            )

            uow.ledgeraccountrepo.create_ledger(
                wallet_withdrawable_account
            )

            return {'message':'you have deposited money into your account'}
        except Exception as e:
            return HTTPException(
                detail=str(e),
                status_code=400
            )

# this will be using mpesa disbursal method 
# we add our transaction fees here for the cash made as well 

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
    

def authorize_wallet_withdrawal_handler(command,uow):
    #this is the function that authorizes the step proecss 
    #retrive teh phone number by geting the user profile and fetching teh phone numer
    #the method to disburse money from mpesa 

    pass 
    
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


def authorize_wallet_transfer_handler(command,uow):
    with uow as uow:
        #get the wallet by user id 
        #the contract must contain the from wallet to wallet and user_id
        #verify pin 
        pass 

def get_wallet_statements(wallet,uow):
    with uow as uow:
        pass 
        #statements=uow.transrepo.get_
def send_message(wallet,uow):
    print('messag is that your have created your wallet')
    print('this is it with balance',wallet.balance)


def process_payment_callback(message,uow):
    payload=message.request.json()
    payment_callback=payload.get("Result")

    print(payment_callback)
    if not payment_callback:
        return {}
    conversation_id=payment_callback.get("ConversationID")
    transaction_id=payment_callback.get('TransactionID')
    result_code=payment_callback.get('ResultCode')
    #find the transaction wit the checkout id
    transaction=message.db.query(Transaction).filter(
        Transaction.checkout_id==conversation_id).first()
    if not transaction:
        return {"ResultCode": 0, 
                "ResultDesc": "Transaction not found"}
    #claim = transaction.claim 
    if result_code == 0:
        transaction.status = "successful"
        transaction.mpesa_receipt = transaction_id

        #if claim:
        #    claim.status = "paid"
    else:
        transaction.status = "failed"
        #if claim:
         #   claim.status = "failed"
    db.commit()
    return {"ResultCode": 0, "ResultDesc": "Success"}


def mpesa_callback(message,uow):
    payload =  message.request.json()

    stk = payload["Body"]["stkCallback"]
    checkout_id = stk["CheckoutRequestID"]
    result_code = stk["ResultCode"]

    transaction = message.db.query(Transaction).filter(
        Transaction.checkout_request_id == checkout_id
    ).first()

    if not transaction:
        return {"ResultCode": 0, "ResultDesc": "Accepted"}

    if result_code == 0:
        transaction.status = "completed"
        # TODO: create accounting entries here
    else:
        transaction.status = "failed"

    db.commit()

    # Safaricom expects THIS
    return {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }