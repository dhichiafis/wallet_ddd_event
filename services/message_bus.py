from typing import List,Union
from models.event import *
from models.command import *
from services.user_handler import *
from services.wallet_handler import *
from services.unitofwork import *

Message=Union[Command,Event]




COMMANDS={
    RegisterUser:create_user,
    CreateWallet:create_wallet_handler,
    DepositToWallet:deposit_to_wallet_handler,
    WithdrawFromWallet:withdraw_from_wallet_handler
}

EVENTS={
    UserCreated:[],
    WalletCreated:[send_message],
    TransactionCreated:[],
}

def handle(message:Message,uow:UnitOfWork):
    result=[]
    queue=[message]
    
    while queue:
        message=queue.pop(0)
        if isinstance(message,Command):
            resultCommand=handle_command(command=message,queue=queue,uow=uow)
            result.append(resultCommand)
        elif isinstance(message,Event):
            handle_events(event=message,queue=queue,uow=uow)
        
    return result



def handle_events(event,queue,uow):
    for handler in EVENTS[type(event)]:
        handler(event,uow)
        queue.extend(uow.collect_events())




def handle_command(command,queue,uow):
    handler=COMMANDS[type(command)]
    result=handler(command,uow)
    queue.extend(uow.collect_events())
    return result 