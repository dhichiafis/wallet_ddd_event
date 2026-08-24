from sqlalchemy.orm import Session ,sessionmaker 
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from models.domain import *
from sqlalchemy import Table,Column,Integer,ForeignKey,Boolean,String,DateTime,Numeric

url='sqlite:///first2134uy6uuii.db'
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
wallet_table = Table(
    "wallets",
    registry.metadata,

    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, nullable=False),
    Column("balance", Numeric, nullable=False),
    Column("pin", String, nullable=False),
    Column("created_at", DateTime)
)
#wallet_table=Table(
 #   'wallets',
  #  registry.metadata,

#)

transaction_table=Table(
    'transactions',
    registry.metadata,
    Column('transaction_id',Integer,primary_key=True),
    Column(
        'wallet_id',
        Integer,
        ForeignKey('wallets.id'),
        nullable=False
    ),
    #reference number to reference or index the transaction

    #membership this can be sacco member ,shop number or customer number in reference to the business
    Column('type',String),
    #channel type can be a bank transfer pesa link ,mpesa  or cash moeny
    Column('description',String),
    Column('amount',Numeric),
    Column('created_at',DateTime)
)

transfer_table = Table(
    'transfers',
    registry.metadata,

    Column('id', Integer, primary_key=True),

    Column(
        'from_wallet',
        Integer,
        ForeignKey('wallets.id'),
        nullable=False
    ),

    Column(
        'to_wallet',
        Integer,
        ForeignKey('wallets.id'),
        nullable=False
    ),

    Column('amount', Numeric, nullable=False),
    Column('status', String, nullable=False),
    Column('created_at', DateTime, nullable=False)
)
        
journal_entry_table=Table(
     'journal_entries',
    registry.metadata,
    Column('journalentry_id',Integer,primary_key=True),
    Column('created_at',DateTime),
    Column('description',String)
)


journalentrylines_table=Table(
     'journalentrylines',
     registry.metadata,
     Column('journalentryline_id',Integer,primary_key=True),
     Column('journalentry_id',Integer,ForeignKey('journal_entries.journalentry_id')),
     Column('debit',Numeric),
     Column('credit',Numeric),
     Column('account_id',Integer),
     Column('account_name',String)
)

ledgeraccount_table=Table(
    'ledgeraccounts',
    registry.metadata,
    Column('ledgeracc_id',Integer,primary_key=True),
    Column('ledgeraccountname',String),
    Column('type',String),
    Column('created_at',DateTime)

)

ledgeraccline_table=Table(
    'ledgeraccountlines',
    registry.metadata,
    Column('ledgeraccountlines_id',Integer,primary_key=True),
    Column('ledgeraccount_id',Integer,ForeignKey('ledgeraccounts.ledgeracc_id')),
    Column('membership',String,unique=True),
    Column('description',String),
    Column('debit',Numeric),
    Column('credit',Numeric),
)


registry.map_imperatively(
    JournalEntry,
    journal_entry_table,
    properties={
        "lines": relationship(
            JournalEntryLine,
            cascade="all, delete-orphan",
            back_populates="journal_entry"
        )
    }
)

registry.map_imperatively(
    JournalEntryLine,
    journalentrylines_table,
    properties={
        "journal_entry": relationship(
            JournalEntry,
            back_populates="lines"
        )
    }
)

#registry.map_imperatively(Transaction,transaction_table)
registry.map_imperatively(
    Transaction,
    transaction_table,
    properties={
        "wallet": relationship(
            Wallet,
            back_populates="transactions"
        )
    }
)
registry.map_imperatively(LedgerAccount,ledgeraccount_table)
registry.map_imperatively(LedgerAccountLines,ledgeraccline_table)
registry.map_imperatively(
    Transfer,
    transfer_table
)
registry.map_imperatively(User,user_table)
#registry.map_imperatively(Wallet,wallet_table)
registry.map_imperatively(
    Wallet,
    wallet_table,
    properties={
        "transactions": relationship(
            Transaction,
            back_populates="wallet"
        )
    }
)
registry.metadata.create_all(bind=engine)


def connect():
    db=SessionFactory()
    try:
        yield db 
    finally:
        db.close()