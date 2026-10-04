from fastapi  import APIRouter,Depends,status,HTTPException,Request
from models.command import *
from services.wallet_handler import *
from services.unitofwork import *
from services.message_bus import *
from security import *
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from infrastructure.rate_limiter import *
transaction_router=APIRouter(
    prefix='/transactions',
    tags=['transactions']

)



@transaction_router.get('/all')
async def get_all_transactions():
    uow=UnitOfWork()
    with uow as uow:
        transactions=uow.transrepo.get_all_transactions()
        return [{
            "transaction_id":transaction.transaction_id,
            "wallet_id":transaction.wallet_id,
            "type":transaction.type,
            "description":transaction.description,
            "amount":transaction.amount,
            "status":transaction.status,
            "mpesa_reciept":transaction.mpesa_reciept,
            "checkout_id":transaction.checkout_id,
            "created_at":transaction.created_at
        }
        for transaction in transactions]

@transaction_router.get("/wallet")
async def get_transaction_by_wallet(
    user:User=Depends(get_current_active_user)
):
    uow=UnitOfWork()
    with uow as uow:
        wallet=uow.walletrepo.get_wallet_by_user_id(
            user_id=user.id
        )
        transactions=uow.transrepo.get_wallet_transactions(wallet_id=wallet.id)
        return [{
            "transaction_id":transaction.transaction_id,
            "wallet_id":transaction.wallet_id,
            "type":transaction.type,
            "description":transaction.description,
            "amount":transaction.amount,
            "status":transaction.status,
            "mpesa_reciept":transaction.mpesa_reciept,
            "checkout_id":transaction.checkout_id,
            "created_at":transaction.created_at
        }for transaction in transactions]

@transaction_router.get("/deposit/status/{checkout_id}")
async def check_deposit_status(
    payload:FetchTransactionRequest,
):
    uow = UnitOfWork()
    command=FetchTransaction(
        checkout_id=payload.checkout_id
    )
    return handle(message=command,uow=uow)


#@transaction_router.get("/status")
async def fetch_transaction_by_status(
    status:str,
):
    uow = UnitOfWork()
    command=FetchTransactionByStatus(
        status=status
    )
    return handle(message=command,uow=uow)