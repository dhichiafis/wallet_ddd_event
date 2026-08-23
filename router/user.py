from fastapi import APIRouter,Depends,HTTPException
from models.command import *
from models.event import *
from services.unitofwork import *
from services.user_handler import *
from services.message_bus import *

user_router=APIRouter(prefix='/users',tags=['users'])
# the message bus is responsible for handling the command to create the user 

@user_router.post('/new')
async def register_user(
    payload:RegisterUser
):
    uow=UnitOfWork()
    return handle(message=payload,uow=uow)



@user_router.post('/token')
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm=Depends(),
    db:Session=Depends(connect)
) -> Token:
    return login_user(db=db,form_data=form_data)


@user_router.get('/all')
async def get_all_users(

):
    uow=UnitOfWork()
    return get_all_users_handler(uow=uow)


@user_router.get("/me", response_model=UserBase)
async def read_users_me(
    current_user:User=Depends(get_current_active_user),
):
    return current_user

