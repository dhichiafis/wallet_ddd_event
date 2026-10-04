from FastAPI import HTTPException,status

def fetch_transaction_by_status(message,uow):
    with uow as uow:
        transaction=uow.transrepo.get_transaction_by_status()
        if not transaction:
            raise HTTPException(
                detail=str('the transaction does not exist'),
                status_code=400
            )
        return {
            'transaction_id':transaction.transaction_id,
            'wallet_id':transaction.wallet_id,
            'type':transaction.type,
            'description':transaction.description,
            'amount ':transaction.amount,
            'status':transaction.status,
            'mpesa_reciept':transaction.reciept,
            'checkout_id':transaction.checkout_id,
            'created_at ':transaction.created_at,
 
        }