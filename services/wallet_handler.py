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

        uow.profilerepo.add_profile(profile)
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

def deposit_to_wallet_handler(command, uow):

    with uow as uow:

        mywallet = uow.walletrepo.get_wallet_by_user_id(
            user_id=command.user_id
        )

        if mywallet is None:
            raise ValueError("Wallet does not exist")

        profile = uow.profilerepo.get_profile_by_user_id(
            user_id=command.user_id
        )

        if profile is None:
            raise ValueError("User profile does not exist")

        if not profile.phonenumber:
            raise ValueError("Phone number is not registered")

        transaction = Transaction(
            transaction_id=None,
            wallet_id=mywallet.id,
            type="deposit",
            description=f"Deposit to wallet {mywallet.id}",
            amount=command.amount,
            status="pending",
            mpesa_reciept=None,
            checkout_id=None,
            created_at=datetime.now(
                ZoneInfo("Africa/Nairobi")
            )
        )

        # PhoneNumber -> string
        phone_number = str(profile.phonenumber)

        # Send ONE STK Push
        response = send_prompt_push(
            phone_number=phone_number,
            amount=transaction.amount
        )

        print("STK RESPONSE:", response)

        if response.get("ResponseCode") != "0":
            raise ValueError(
                f"STK Push failed: {response}"
            )

        checkout_id = response.get(
            "CheckoutRequestID"
        )

        if not checkout_id:
            raise ValueError(
                "Safaricom did not return CheckoutRequestID"
            )

        # Connect Safaricom request to our transaction
        transaction.checkout_id = checkout_id

        # Persist pending transaction
        uow.transrepo.create_transaction(transaction)

        uow.commit()

        return {
            "message": "STK push sent",
            "status": "pending",
            "checkout_id": checkout_id
        }

#
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
    message.db.commit()
    return {"ResultCode": 0, "ResultDesc": "Success"}

#these are not used to change the state of transaction

def mpesa_callback(message, uow):

    with uow as uow:

        payload = message.payload

        stk = payload["Body"]["stkCallback"]

        checkout_id = stk["CheckoutRequestID"]
        result_code = stk["ResultCode"]

        transaction = uow.transrepo.get_by_checkout_id(
            checkout_id=checkout_id
        )

        if transaction is None:
            raise ValueError(
                f"Transaction not found: {checkout_id}"
            )

        if result_code != 0:

            transaction.status = "failed"

            uow.commit()

            return {
                "ResultCode": 0,
                "ResultDesc": "Accepted"
            }

        callback_metadata = stk.get(
            "CallbackMetadata",
            {}
        )

        items = callback_metadata.get(
            "Item",
            []
        )

        mpesa_receipt = None

        for item in items:

            if item.get("Name") == "MpesaReceiptNumber":
                mpesa_receipt = item.get("Value")
                break

        if not mpesa_receipt:
            raise ValueError(
                "M-Pesa receipt was not returned"
            )
        wallet = uow.walletrepo.get_wallet_by_id(
            wallet_id=transaction.wallet_id
        )

        if wallet is None:
            raise ValueError("Wallet not found")

        wallet.deposit(
            amount=transaction.amount
        )
        transaction.status = "successful"

        transaction.mpesa_receipt = mpesa_receipt

       
        cash_account = (
            uow.ledgeraccrepo
            .get_by_ledger_account_name(
                "Cash Account"
            )
        )

        if cash_account is None:
            raise ValueError(
                "Cash Account does not exist"
            )

        wallet_account = (
            uow.ledgeraccrepo
            .get_by_ledger_account_name(
                "Wallet Withdrawable Account"
            )
        )

        if wallet_account is None:
            raise ValueError(
                "Wallet Withdrawable Account "
                "does not exist"
            )

        journal_entry = JournalEntry(
            journalentry_id=None,
            description=(
                f"Deposit of {transaction.amount} "
                f"to wallet {transaction.wallet_id}"
            ),
            created_at=datetime.now(
                ZoneInfo("Africa/Nairobi")
            )
        )

        cash_line = JournalEntryLine(
            journalentryline_id=None,
            wallet_id=transaction.wallet_id,
            account_name=(
                cash_account.ledgeraccountname
            ),
            debit=transaction.amount,
            credit=Decimal("0")
        )
        wallet_line = JournalEntryLine(
            journalentryline_id=None,
            wallet_id=transaction.wallet_id,
            account_name=(
                wallet_account.ledgeraccountname
            ),
            debit=Decimal("0"),
            credit=transaction.amount
        )

        journal_entry.add_lines(cash_line)
        journal_entry.add_lines(wallet_line)
        if not journal_entry.valid_entry():
            raise ValueError(
                "Journal entry is not balanced"
            )
        cash_ledger_line = LedgerAccountLines(
            ledgeraccountlines_id=None,
            wallet_id=transaction.wallet_id,
            description=(
                f"Cash received for deposit "
                f"{transaction.transaction_id}"
            ),
            debit=transaction.amount,
            credit=Decimal("0")
        )

        cash_account.post_to_ledger(
            cash_ledger_line
        )
        wallet_ledger_line = LedgerAccountLines(
            ledgeraccountlines_id=None,
            wallet_id=transaction.wallet_id,
            description=(
                f"Wallet withdrawable created for "
                f"transaction {transaction.transaction_id}"
            ),
            debit=Decimal("0"),
            credit=transaction.amount
        )

        wallet_account.post_to_ledger(
            wallet_ledger_line
        )
        uow.journalrepo.create_journal_entry(
            journal_entry
        )
        uow.ledgeraccountrepo.create_ledger(
            cash_account
        )

        uow.ledgeraccountrepo.create_ledger(
            wallet_account
        )
        #-----
        uow.commit()

        return {
            "ResultCode": 0,
            "ResultDesc": "Accepted"
        }