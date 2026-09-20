from fastapi import FastAPI 
from router.user import *
from router.wallet import *
from router.profile import *
import uvicorn 
from slowapi import _rate_limit_exceeded_handler
from infrastructure.rate_limiter import *

app=FastAPI()
app.state.limiter=limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

app.include_router(user_router)
app.include_router(profile_router)
app.include_router(wallet_router)


@app.get('/')
async def healthcheck():
    return {'message':'welcome to wallet'}