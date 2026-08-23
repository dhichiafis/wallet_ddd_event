from models.domain import *

class JournalEntryRepository:
    def __init__(self,session):
        self.session=session
        self.seen=set()
    def create_journal_entry(self,entry):
        self.session.add(entry)
        self.seen.add(entry)

    def get_all_journal_entries(self):
        return self.session.query(JournalEntry).all()
    
    def get_journal_entry_by_id(self,id):
        return self.session.query(JournalEntry).filter(JournalEntry.id==id).first()