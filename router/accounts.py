from fastapi  import APIRouter,Depends,status,HTTPException,Request
from models.command import *
from services.wallet_handler import *
from services.unitofwork import *
from services.message_bus import *
from security import *
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from infrastructure.rate_limiter import *
accounts_router=APIRouter(
    prefix='/accounts',
    tags=['accountss']
)


@accounts_router.get('/all')
async def get_all_accounts():
    uow=UnitOfWork()
    with uow as uow:
        accounts=uow.ledgeraccrepo.get_all_ledgers()
        return [

            {
            "ledgeraccountname":account.ledgeraccountname,
            "type":account.type
                    
            }for account in accounts
        ]

@accounts_router.get('/name')
async def get_account_balance(account_name):
    uow=UnitOfWork()
    with uow as uow:
        balance=uow.ledgeraccrepo.get_balance(account_name=account_name)
        return balance


@accounts_router.get("/ledger/accounts/{ledger_account_id}")
def get_ledger_account(
    ledger_account_id: int,
    db: Session = Depends(connect)
):
    account = (
        db.query(LedgerAccount)
        .filter(
            LedgerAccount.ledgeracc_id == ledger_account_id
        )
        .first()
    )

    if account is None:
        raise HTTPException(
            status_code=404,
            detail="Ledger account not found"
        )

    return {
        "account_id": account.ledgeracc_id,
        "account_name": account.ledgeraccountname,
        "account_type": account.type,
        "lines": [
            {
                "id": line.ledgeraccountlines_id,
                "wallet_id": line.wallet_id,
                "description": line.description,
                "debit": line.debit,
                "credit": line.credit,
            }
            for line in account.ledgeraccount_lines
        ]
    }

@accounts_router.get("/ledger/balance-sheet")
def get_balance_sheet(
    #as_at: datetime,
    db: Session = Depends(connect)
):
    accounts = (
        db.query(LedgerAccount)
        .all()
    )

    assets = []
    liabilities = []
    equity = []

    for account in accounts:

        total_debit = sum(
            (line.debit or Decimal("0"))
            for line in account.ledgeraccount_lines
            #if line.created_at <= as_at
        )

        total_credit = sum(
            (line.credit or Decimal("0"))
            for line in account.ledgeraccount_lines
            #if line.created_at <= as_at
        )

        if account.type == "Asset":
            balance = total_debit - total_credit
            assets.append({
                "account_id": account.ledgeracc_id,
                "account_name": account.ledgeraccountname,
                "balance": balance
            })

        elif account.type == "Liability":
            balance = total_credit - total_debit
            liabilities.append({
                "account_id": account.ledgeracc_id,
                "account_name": account.ledgeraccountname,
                "balance": balance
            })

        elif account.type == "Equity":
            balance = total_credit - total_debit
            equity.append({
                "account_id": account.ledgeracc_id,
                "account_name": account.ledgeraccountname,
                "balance": balance
            })

    total_assets = sum(
        item["balance"] for item in assets
    )

    total_liabilities = sum(
        item["balance"] for item in liabilities
    )

    total_equity = sum(
        item["balance"] for item in equity
    )

    return {
        
        "assets": assets,
        "total_assets": total_assets,
        "liabilities": liabilities,
        "total_liabilities": total_liabilities,
        "equity": equity,
        "total_equity": total_equity,
        "total_liabilities_and_equity":
            total_liabilities + total_equity,
        "balanced":
            total_assets ==
            total_liabilities + total_equity
    }