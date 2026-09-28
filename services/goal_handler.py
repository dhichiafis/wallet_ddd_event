from models.domain import *
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import HTTPException
from services.payments import *


def create_goal_handler(
        message,
        uow
):
    with uow as uow:
        #wallet=uow.walletrepo.get_wallet
        wallet=uow.walletrepo.get_wallet_by_user_id(user_id=message.user_id)
        if wallet is None:
            raise HTTPException(
                status_code=404,
                detail="Wallet not found"
            )

        if message.initial_amount <= 0:
            raise HTTPException(
                status_code=400,
                detail="Initial contribution must be greater than zero"
            )
        
        if message.initial_amount<=1000:
            raise HTTPException(
                status_code=400,
                detail='The initial contribution cannot be less than 1000'
            )
        
        if message.initial_amount > message.target_amount:
            raise HTTPException(
                status_code=400,
                detail="Initial contribution cannot exceed goal target"
            )

        # This checks wallet balance AND deducts the money
        wallet.withdraw(message.initial_amount)
        goal=Goal(
            goal_id=None,
            wallet_id=wallet.id,
            goal_name=message.goal_name,
            target_amount=message.target_amount,
            target_duration=message.target_duration,
            purpose=message.purpose,
            created_at=datetime.now(ZoneInfo('Africa/Nairobi')),
            updated_at=datetime.now(ZoneInfo('Africa/Nairobi'))
        )
        contribution = GoalContributions(
            goal_contribution_id=None,
            goal_id=None,
            contribution_amount=message.initial_amount,
            contribution_date=datetime.now(
                ZoneInfo("Africa/Nairobi")
            )
        )
        goal.add_contribution(contribution)
        wallet.create_goal(goal)
        transaction=Transaction(
            transaction_id=None,
            wallet_id=wallet.id,
            type='',
            description='',
            amount=contribution.contribution_amount,
            status='complete',
            mpesa_reciept='none',
            checkout_id='none',
            created_at=datetime.now(ZoneInfo('Africa/Nairobi'))
        )

        uow.transrepo.create_transaction(transaction)
        # 6. Create accounting journal
        journal = JournalEntry(
            journalentry_id=None,
            description=f"Initial contribution to {goal.goal_name}",
            created_at=datetime.now(
                ZoneInfo("Africa/Nairobi")
            )
        )

        # Goal side
        goal_line = JournalEntryLine(
            journalentryline_id=None,
            wallet_id=wallet.id,
            account_name="Goal Account",
            debit=contribution.contribution_amount,
            credit=0
        )

        # Cash/wallet side
        cash_line = JournalEntryLine(
            journalentryline_id=None,
            wallet_id=wallet.id,
            account_name="Cash Account",
            debit=0,
            credit=contribution.contribution_amount
        )

        journal.add_lines(goal_line)
        journal.add_lines(cash_line)

        if not journal.valid_entry():
            raise ValueError(
                "Journal entry is not balanced"
            )

        uow.journalrepo.create_journal_entry(journal)
        goal_account = uow.ledgerrepo.get_account_by_name(
            "Goal Account"
            )   

        cash_account = uow.ledgerrepo.get_account_by_name(
            "Cash Account"
        )

        if goal_account is None:
            raise ValueError("Goal Account does not exist")

        if cash_account is None:
            raise ValueError("Cash Account does not exist")
       
        goal_ledger_line = LedgerAccountLines(
            ledgeraccountlines_id=None,
            ledgeraccount_id=goal_account.ledgeracc_id,
            wallet_id=wallet.id,
            description=f"Initial contribution to {goal.goal_name}",
            debit=contribution.contribution_amount,
            credit=0
        )

        cash_ledger_line = LedgerAccountLines(
            ledgeraccountlines_id=None,
            ledgeraccount_id=cash_account.ledgeracc_id,
            wallet_id=wallet.id,
            description=f"Initial contribution to {goal.goal_name}",
            debit=0,
            credit=contribution.contribution_amount
            )

        uow.ledgerrepo.add_line(goal_ledger_line)
        uow.ledgerrepo.add_line(cash_ledger_line)
        #uow.goalrepo.create_goal(goal)
       
        
        uow.commit()
        return {'message':'goal created successfully'}


def run_daily_goals():
    pass 