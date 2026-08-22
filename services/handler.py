from fastapi import HTTPException
from datetime import datetime
from zoneinfo import ZoneInfo
from security import *
def create_user(user,uow):
    with uow as uow:
        
        existing_user=uow.userrepo.get_user_by_username(username=user.username)
        if existing_user:
            raise HTTPException(
                detail='user already exist',
                status_code=400
            )
           
        password=get_password_hash(user.password)
        new_user=User(
            id=None,
            username=user.username,
            password=password,is_active=True,
            created_at=datetime.now(ZoneInfo("Africa/Nairobi"))
            ,updated_at=datetime.now(ZoneInfo('Africa/Nairobi'))
            )
            #raising an event
        try:
            uow.userrepo.create_user(new_user)
            uow.commit()
            return {'message':'user created '}
        except Exception as e:
            return str(e)