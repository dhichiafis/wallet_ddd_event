from fastapi  import APIRouter,Depends,status,HTTPException,Request
from models.command import *
from services.wallet_handler import *
from services.unitofwork import *
from services.message_bus import *
from security import *
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from infrastructure.rate_limiter import *
goal_router=APIRouter(
    prefix='/goals',
    tags=['goals']
)


@goal_router.post('/new')
async def create_new_goal(
    payload:CreateGoal,
    user:User=Depends(get_current_active_user)
):
    uow=UnitOfWork()
    mes=CreateGoalRequest(
        user_id=user.id,
        goal_name=payload.goal_name,
        target_amount=payload.target_amount,
        target_duration=payload.target_duration,
        initial_amount=payload.initial_amount,
        purpose=payload.purpose
    )

    return handle(message=mes,uow=uow)

@goal_router.get('/all')
async def get_all_goals():
    uow=UnitOfWork()
    with uow:
        goals= uow.goalrepo.get_all_goals()
        return [{
            "goal_id": goal.goal_id,
            "wallet_id": goal.wallet_id,
            "goal_name": goal.goal_name,
            "target_amount": goal.target_amount,
            "target_duration": goal.target_duration,
            "purpose": goal.purpose,
            "created_at": goal.created_at,
            "updated_at": goal.updated_at,
        } for goal in goals]

#@goal_router.get('/{goal_id}')
async def get_goal_by_id(goal_id):
    pass 


#@goal_router.get('/wallet')
async def get_all_goals(
    user: User = Depends(get_current_active_user)
):
    uow = UnitOfWork()

    with uow:
        wallet = uow.walletrepo.get_wallet_by_user_id(
            user_id=user.id
        )

        if wallet is None:
            raise HTTPException(
                status_code=404,
                detail="Wallet not found"
            )

        goals = wallet.goals

        return goals

@goal_router.get('/wallet')
async def get_wallet_goals(
    user: User = Depends(get_current_active_user)
):
    uow = UnitOfWork()

    with uow:
        wallet = uow.walletrepo.get_wallet_by_user_id(
            user_id=user.id
        )

        if wallet is None:
            raise HTTPException(
                status_code=404,
                detail="Wallet not found"
            )

        return [
            {
                "goal_id": goal.goal_id,
                "wallet_id": goal.wallet_id,
                "goal_name": goal.goal_name,
                "target_amount": goal.target_amount,
                "target_duration": goal.target_duration,
                "purpose": goal.purpose,
                "created_at": goal.created_at,
                "updated_at": goal.updated_at,
            }
            for goal in wallet.goals
        ]


@goal_router.get('/{goal_id}')
async def get_goal_by_id(goal_id: int):
    pass