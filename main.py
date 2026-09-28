from fastapi import FastAPI 
from router.user import *
from router.wallet import *
from router.profile import *
from router.goal import *
from router.transactions import *
from router.accounts import *
import uvicorn 
from slowapi import _rate_limit_exceeded_handler
from infrastructure.rate_limiter import *
from infrastructure.database import *

from sqlalchemy.orm import Session 

app=FastAPI()

initialize_accounts()
app.state.limiter=limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

app.include_router(user_router)
app.include_router(profile_router)
app.include_router(wallet_router)
app.include_router(accounts_router)
app.include_router(transaction_router)
app.include_router(goal_router)



@app.get('/')
async def healthcheck():
    return {'message':'welcome to wallet'}