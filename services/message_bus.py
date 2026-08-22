from typing import List,Union
from models.event import *
from models.command import *
from services.handler import *
from services.unitofwork import *

Message=Union[Command,Event]




COMMANDS={
    RegisterUser:create_user
}

EVENTS={
    UserCreated:[]
}

def handle(message:Message,uow:UnitOfWork):
    result=[]
    queue=[message]
    
    while queue:
        message=queue.pop[0]
        if isinstance(message,Command):
            handle_command(command=message,queue=queue,uow=uow)
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