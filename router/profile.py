from fastapi  import APIRouter,Depends,status,HTTPException,Request
from models.command import *
from services.wallet_handler import *
from services.unitofwork import *
from services.message_bus import *
from security import *
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from infrastructure.rate_limiter import *
profile_router=APIRouter(
    prefix='/profile',
    tags=['profile']
)

'''
@profile_router.post('/new')
async def create_profile(
    payload:CreateProfileRequest,
    user:User=Depends(get_current_active_user)
):
    uow=UnitOfWork()
    command=CreateProfile(
        user_id=user.id,
        firstname=payload.firstname,
    lastname=payload.lastname,
    phonenumber=payload.phonenumber
        
    )
    return handle(message=command,uow=uow)

'''

@profile_router.post('/register')
async def register_profile(
    payload:CompleteRegistration,
    user:User=Depends(get_current_active_user)
):
    uow=UnitOfWork()
    command=CompleteRegistration(
        user_id=user.id,
        firstname=payload.firstname,
        lastname=payload.lastname,
        phonenumber=payload.phonenumber,
        pin=payload.pin
    )
    return handle(message=command,uow=uow)