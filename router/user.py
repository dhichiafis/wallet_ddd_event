from fastapi import APIRouter,Depends,HTTPException
from models.command import *
from models.event import *
from services.unitofwork import *
from services.handler import *

user_router=APIRouter(prefix='/users',tags=['users'])


@user_router.post('/new')
async def register_user(
    payload:RegisterUser
):
    uow=UnitOfWork()
    create_user(user=payload,uow=uow)



@user_router.post('/login')
async def login():
    pass 

