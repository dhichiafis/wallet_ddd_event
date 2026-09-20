from fastapi import APIRouter,Depends,HTTPException,Request
from models.command import *
from models.event import *
from services.unitofwork import *
from services.user_handler import *
from services.message_bus import *
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from infrastructure.rate_limiter import *



user_router=APIRouter(prefix='/users',tags=['users'])

# the message bus is responsible for handling the command to create the user 
# the rate limiter protects teh service from geting overloaded with request while providing fair usage

@user_router.post('/new')

async def register_user(
    payload:RegisterUser
):
    uow=UnitOfWork()
    return handle(message=payload,uow=uow)



@user_router.post('/token')
#@limiter.limit("8/minute")
async def login_for_access_token(
    request:Request,
    form_data: OAuth2PasswordRequestForm=Depends(),
    db:Session=Depends(connect)
) -> Token:
    return login_user(db=db,form_data=form_data)


@user_router.get('/all')
@limiter.limit("2/minute")
async def get_all_users(
   #payload:GetAllUser,
   request:Request
):
    payload=GetAllUser()
    uow=UnitOfWork()
    return handle(message=payload,uow=uow)
    #return get_all_users_handler(command=payload,uow=uow)

@user_router.get("/me", response_model=UserBase)
async def read_users_me(
    current_user:User=Depends(get_current_active_user),
):
    return current_user

@user_router.delete("/delete")
async def delete_user(
    username:str,
    db:Session=Depends(connect)
):
    user=db.query(User).filter(User.username==username).first()
    if not user:
        raise HTTPException(detail='user does not exist',status_code=400)
    db.delete(user)
    db.commit()
    return {'message':f"user {username} deleted successfully"}
    
