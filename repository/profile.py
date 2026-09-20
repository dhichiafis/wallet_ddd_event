
from models.domain import *
class ProfileRepository:
    def __init__(self,session):
        self.session=session 
        self.seen=set()

    def add_profile(self,profile):
        #print("addd",user)
        self.session.add(profile)
        self.seen.add(profile)

    def get_all_profiles(self):
        return self.session.query(Profile).all()

    def get_profile_by_id(self,id):
        
        return self.session.query(Profile).filter(Profile.id==id).first()

    def get_profile_by_user_id(self,user_id):
        return self.session.query(Profile).filter(Profile.user_id==user_id).first()