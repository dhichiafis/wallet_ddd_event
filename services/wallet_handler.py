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

#this method has to invoke the stk push 
#teh thing is that the changes made here are that we are not modifying the source of truth
def deposit_to_wallet_handlerv1(wallet,uow):
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
            status='pending',
            mpesa_reciept='None',
            checkout_id='None',
            created_at=datetime.now(ZoneInfo('Africa/Nairobi'))
        )
            profile = uow.profilerepo.get_profile_by_user_id(
                user_id=wallet.user_id      
            )

            if profile is None:
                raise ValueError("User profile does not exist")
 
            if not profile.phonenumber:
                raise ValueError("Phone number is not registered")

            phonenumber=profile.phonenumber
            send_prompt_push(phone_number=phonenumber,amount=transaction.amount)
            response = send_prompt_push(
            phone_number=phonenumber,
            amount=wallet.amount
        )

            print("STK RESPONSE:", response)

            if response.get("ResponseCode") != "0":
                raise ValueError(
                f"STK Push failed: {response}"
                )

            checkout_id = response.get("CheckoutRequestID")

            uow.transrepo.create_transaction(transaction)
            print("CREATED TRANSACTION")
            print("ID:", transaction.transaction_id)
            print("WALLET ID:", transaction.wallet_id)
            print("TYPE:", transaction.type)
            print("AMOUNT:", transaction.amount)

            
            
            uow.commit()
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
        uow.commit()
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
    message.db.commit()
    return {"ResultCode": 0, "ResultDesc": "Success"}

#these are not used to change the state of transaction

def mpesa_callback(message, uow):
    with uow as uow:
        payload = message.payload

        stk = payload["Body"]["stkCallback"]

        checkout_id = stk["CheckoutRequestID"]
        result_code = stk["ResultCode"]

    

    # ------------------------------------------------
    # 1. Find our transaction
    # ------------------------------------------------

    
        transaction = uow.transrepo.get_by_checkout_id(checkout_id=checkout_id)
    

        if transaction is None:
            return {
            "ResultCode": 0,
            "ResultDesc": "Accepted"
        }

    # ------------------------------------------------
    # 2. Idempotency protection
    # ------------------------------------------------

        if transaction.status == "completed":
            return {
            "ResultCode": 0,
            "ResultDesc": "Accepted"
        }

    # ------------------------------------------------
    # 3. Failed M-Pesa payment
    # ------------------------------------------------

        if result_code != 0:

            transaction.status = "failed"

            uow.commit()

            return {
            "ResultCode": 0,
            "ResultDesc": "Accepted"
        }

    # ------------------------------------------------
    # 4. Successful M-Pesa payment
    # ------------------------------------------------

        wallet = uow.walletrepo.get_wallet_by_id(
        wallet_id=transaction.wallet_id
    )

        if wallet is None:
            raise ValueError("Wallet not found")

    # ------------------------------------------------
    # 5. Extract M-Pesa receipt
    # ------------------------------------------------

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

    # ------------------------------------------------
    # 6. Update wallet
    # ------------------------------------------------

        wallet.deposit(
        amount=transaction.amount
    )

    # ------------------------------------------------
    # 7. Update transaction
    # ------------------------------------------------

        transaction.status = "completed"
        transaction.mpesa_receipt = mpesa_receipt
        transaction.status = "completed"

        print("====== BEFORE ACCOUNTING ======")
        print("Transaction:", transaction.id)
        print("Transaction status:", transaction.status)
        print("Transaction receipt:", transaction.mpesa_receipt)
        print("Wallet:", wallet.id)
        print("Wallet balance:", wallet.balance)
        print("===============================")

    # ------------------------------------------------
    # 8. Get accounting accounts
    # ------------------------------------------------

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

        wallet_withdrawable_account = (
            uow.ledgeraccrepo
        .get_by_ledger_account_name(
            "Wallet Withdrawable Account"
        )
    )

        if wallet_withdrawable_account is None:
            raise ValueError(
            "Wallet Withdrawable Account does not exist"
        )

    # ------------------------------------------------
    # 9. Create journal entry
    # ------------------------------------------------

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
        account_name=cash_account.ledgeraccountname,
        debit=transaction.amount,
        credit=Decimal("0")
    )

        wallet_line = JournalEntryLine(
        journalentryline_id=None,
        wallet_id=transaction.wallet_id,
        account_name=(
            wallet_withdrawable_account
            .ledgeraccountname
        ),
        debit=Decimal("0"),
        credit=transaction.amount
    )

        journal_entry.add_lines(cash_line)
        journal_entry.add_lines(wallet_line)

    # ------------------------------------------------
    # 10. Verify double-entry accounting
    # ------------------------------------------------

        if not journal_entry.valid_entry():

            raise ValueError(
            "Journal entry is not balanced"
        )

    # ------------------------------------------------
    # 11. Create ledger lines
    # ------------------------------------------------

        cash_ledger_line = LedgerAccountLines(
        ledgeraccountlines_id=None,
        wallet_id=transaction.wallet_id,
        description=(
            f"Deposit to wallet "
            f"{transaction.wallet_id}"
        ),
        debit=transaction.amount,
        credit=Decimal("0")
    )

        wallet_ledger_line = LedgerAccountLines(
        ledgeraccountlines_id=None,
        wallet_id=transaction.wallet_id,
        description=(
            f"Deposit to wallet "
            f"{transaction.wallet_id}"
        ),
        debit=Decimal("0"),
        credit=transaction.amount
    )

        cash_account.post_to_ledger(
        cash_ledger_line
    )

        wallet_withdrawable_account.post_to_ledger(
        wallet_ledger_line
    )

    # ------------------------------------------------
    # 12. Persist accounting
    # ------------------------------------------------

        uow.ledgeraccountrepo.create_ledger(
        cash_account
    )

        uow.ledgeraccountrepo.create_ledger(
        wallet_withdrawable_account
    )

    # Also persist the journal entry if your
    # architecture has a journal repository.

    # uow.journalrepo.create_journal_entry(
    #     journal_entry
    # )

    # ------------------------------------------------
    # 13. ONE commit
    # ------------------------------------------------

        uow.commit()

        return {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }

#
'''

a definition of unused callback
def mpesa_callbackn(message, uow):

    payload = message.request.json()

    stk = payload["Body"]["stkCallback"]

    checkout_id = stk["CheckoutRequestID"]
    result_code = stk["ResultCode"]
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
    transaction = (
        message.db.query(Transaction)
        .filter(
            Transaction.checkout_id == checkout_id
        )
        .first()
    )

    if transaction is None:
        return {
            "ResultCode": 0,
            "ResultDesc": "Accepted"
        }

    # Idempotency
    if transaction.status == "completed":
        return {
            "ResultCode": 0,
            "ResultDesc": "Accepted"
        }

    if result_code != 0:

        transaction.status = "failed"

        message.db.commit()

        return {
            "ResultCode": 0,
            "ResultDesc": "Accepted"
        }

    # SUCCESS
    transaction.status = "completed"

    # Extract receipt
    callback_metadata = stk.get(
        "CallbackMetadata",
        {}
    )

    items = callback_metadata.get(
        "Item",
        []
    )

    for item in items:
        if item.get("Name") == "MpesaReceiptNumber":
            transaction.mpesa_receipt = item.get(
                "Value"
            )

    # NOW update wallet
    wallet = (
        message.db.query(Wallet)
        .filter(
            Wallet.id == transaction.wallet_id
        )
        .first()
    )

    if wallet is None:
        raise ValueError("Wallet not found")

    wallet.deposit(transaction.amount)

    # TODO:
    # create journal entry
    # debit Cash
    # credit Wallet Withdrawable
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

    message.db.commit()

    return {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
'''