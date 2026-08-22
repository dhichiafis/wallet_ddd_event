from sqlalchemy.orm import Session ,sessionmaker 
from sqlalchemy.orm import registry

from sqlalchemy import create_engine

from models.domain import *
from sqlalchemy import Table,Column,Integer,Boolean,String,DateTime,Numeric

url='sqlite:///first1.db'
engine=create_engine(url=url)
registry=registry()

SessionFactory=sessionmaker(bind=engine,autoflush=False,autocommit=False)

user_table=Table(
    'users',

    registry.metadata,
     Column('id',Integer,primary_key=True),
        Column('username',String,unique=True),
        Column('password',String),
        Column('is_active',Boolean,default=False),
        Column('created_at',DateTime),
        Column('updated_at',DateTime)  
)
#wallet_table=Table(
 #   'wallets',
  #  registry.metadata,

#)



registry.map_imperatively(User,user_table)
#registry.map_imperatively(Wallet,wallet_table)
registry.metadata.create_all(bind=engine)


def connect():
    db=SessionFactory()
    try:
        yield db 
    finally:
        db.close()