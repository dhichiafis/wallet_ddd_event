
from models.domain import *
class UserRepository:
    def __init__(self,session):
        self.session=session 
        self.seen=set()

    def add_user(self,user):
        #print("addd",user)
        self.session.add(user)
        self.seen.add(user)

    def get_all_users(self):
        return self.session.query(User).all()

    def get_user_by_id(self,id):
        
        return self.session.query(User).filter(User.id==id).first()

    def get_user_by_username1(self,username):
        return self.session.query(User).filter(User.username==username).first()

    def get_user_by_username(self, username):
        print("LOOKING FOR:", username)

        user = self.session.query(User).filter(
        User.username == username
    ).first()

        print("FOUND:", user)

        return user