from models.domain import *
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import HTTPException



def create_profile_handler(profile,uow):
    with uow as uow:

        new_profile=Profile(
            id=None,
            user_id=profile.user_id,
            firstname=profile.firstname,
            lastname=profile.lastname,
            phonenumber=profile.phonenumber,
            created_at=datetime.now(ZoneInfo('Africa/Nairobi'))
        )
        new_profile.validate()
        uow.profilerepo.add(new_profile)
        uow.commit()
        #pass 