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
            password=password,
            is_active=False,
            created_at=datetime.now(ZoneInfo("Africa/Nairobi"))
            ,updated_at=datetime.now(ZoneInfo('Africa/Nairobi'))
            )
            #raising an event
        try:
            uow.userrepo.add_user(new_user)
            #uow.commit()
            return {'message':'user created '}
        except Exception as e:
            return str(e)


def login_user(db,form_data):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
    return Token(access_token=access_token, token_type="bearer")


def get_all_users_handler(command,uow):
    with uow as uow:
        users=uow.userrepo.get_all_users()
        return [{'id':user.id,'username':user.username}for user in users]