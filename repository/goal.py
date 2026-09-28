from models.domain import *

class GoalRepository:
    def __init__(self,session):
        self.session=session
        self.seen=set()
        
    def create_goal(self,goal):
        self.session.add(goal)
        self.seen.add(goal)

    def get_all_goals(self):
        return self.session.query(Goal).all()
    
    def get_goal_by_id(self,goal_id):
        return self.session.query(Goal).filter(Goal.goal_id==goal_id).first()


    