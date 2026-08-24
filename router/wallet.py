from fastapi  import APIRouter,Depends,status,HTTPException
from models.command import *
from services.wallet_handler import *
from services.unitofwork import *
from services.message_bus import *
from security import *
wallet_router=APIRouter(
    prefix='/wallet',
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


@wallet_router.post('/deposit')
async def deposit_to_wallet(
    payload:DepositToWalletRequest,
    user:User=Depends(get_current_active_user)
):
    uow=UnitOfWork()
    command=DepositToWallet(
        amount=payload.amount,
        user_id=user.id
    )
    return handle(message=command,uow=uow)

@wallet_router.post('/transfer')
async def transfer_to_wallet(
    payload:CreateTranferRequest,
    user:User=Depends(get_current_active_user)
):
    uow=UnitOfWork()
    command=CreateTransfer(
        user_id=user.id,
        #from_wallet=payload.from_wallet,
        to_wallet=payload.to_wallet,
        amount=payload.amount,
        #created_at=payload.created_at
    )
    return handle(command,uow)

@wallet_router.post('/withdraw')
async def withdraw_from_wallet(
    payload:WithdrawFromWalletRequest,
    user:User=Depends(get_current_active_user)
):
    uow=UnitOfWork()
    command=WithdrawFromWallet(
        amount=payload.amount,
        user_id=user.id
    )
    return handle(message=command,uow=uow)

@wallet_router.get('/balance')
async def get_wallet_balance(

    db:Session=Depends(connect),
    user:User=Depends(get_current_active_user)):
    wallet=db.query(Wallet).filter(Wallet.user_id==user.id).first()
    return wallet.balance


@wallet_router.get('/statements')
async def get_statements(
    db:Session=Depends(connect),
    user:User=Depends(get_current_active_user)
):
    wallet=db.query(Wallet).filter(Wallet.user_id==user.id).first()
    statements=db.query(Transaction).filter(Transaction.wallet_id==wallet.id).all()
    return [{
        'transaction_id':wallet.transaction_id,
        'amount':wallet.amount,
        'created_at':wallet.created_at
    }for wallet in statements]


@wallet_router.get('/all')
async def get_all_wallets(
    db:Session=Depends(connect)
):
    wallets=db.query(Wallet).all()
    return [{
        'id':wallet.id,
        'balance':wallet.balance,
        'created_at':wallet.created_at
    }for wallet in wallets]