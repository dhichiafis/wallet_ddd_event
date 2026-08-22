from fastapi import FastAPI 
from router.user import *
from router.wallet import *
import uvicorn 


app=FastAPI()
app.include_router(user_router)
app.include_router(wallet_router)


@app.get('/')
async def healthcheck():
    return {'message':'welcome to wallet'}