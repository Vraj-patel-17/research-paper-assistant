from sqlalchemy.orm import Session
from app.models.note import Note
from app.models.paper import Paper
class NoteService:
    def __init__(self, db: Session):
        self.db = db
    def create_note(self,user_id:int,paper_id:int,content:str):
        paper = (self.db.query(Paper)
        .filter(Paper.id == paper_id).first())
        if not paper:
            return None
        note = Note(content=content,user_id=user_id,paper_id=paper_id,)
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)

        return note

    def get_notes_for_paper():
        ...

    def update_note():
        ...

    def delete_note():
        ...