from fastapi  import APIRouter,Depends,status,HTTPException
from models.command import *
from services.wallet_handler import *
from services.unitofwork import *
from services.message_bus import *
from security import *
wallet_router=APIRouter(
    prefix='/tags',
    tags=['wallet']
)


@wallet_router.post('/new')
async def create_wallet(
    payload:CreateWalletRequest,
    user:User=Depends(get_current_active_user)
):
    uow=UnitOfWork()
    command=CreateWallet(
        user_id=user.id,
        balance=payload.balance,
        pin=payload.pin
    )
    return handle(message=command,uow=uow)

@wallet_router.get('/all')
async def get_all_wallets():
    pass 