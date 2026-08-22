from fastapi  import APIRouter,Depends,status,HTTPException


wallet_router=APIRouter(
    prefix='/tags',
    tags=['wallet']
)


@wallet_router.post('/new')
async def create_wallet():
    pass 

@wallet_router.get('/all')
async def get_all_wallets():
    pass 