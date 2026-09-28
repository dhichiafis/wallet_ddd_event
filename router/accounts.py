from fastapi  import APIRouter,Depends,status,HTTPException,Request
from models.command import *
from services.wallet_handler import *
from services.unitofwork import *
from services.message_bus import *
from security import *
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from infrastructure.rate_limiter import *
accounts_router=APIRouter(
    prefix='/accounts',
    tags=['accountss']
)


@accounts_router.get('/all')
async def get_all_accounts():
    uow=UnitOfWork()
    with uow as uow:
        accounts=uow.ledgeraccrepo.get_all_ledgers()
        return [

            {
            "ledgeraccountname":account.ledgeraccountname,
            "type":account.type
                    
            }for account in accounts
        ]

@accounts_router.get('/name')
async def get_account_balance(account_name):
    uow=UnitOfWork()
    with uow as uow:
        balance=uow.ledgeraccrepo.get_balance(account_name=account_name)
        return balance
        