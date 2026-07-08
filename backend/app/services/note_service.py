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

    def get_notes_for_paper(self,paper_id: int,user_id: int,):
        return (self.db.query(Note).filter(
            Note.paper_id == paper_id,
            Note.user_id == user_id,
        ).order_by(Note.updated_at.desc()).all())

    def update_note(self,note_id: int,user_id: int,content: str,):
        note = (self.db.query(Note).filter(
            Note.id == note_id,
            Note.user_id == user_id,).first())
        if not note:
            return None

        note.content = content

        self.db.commit()
        self.db.refresh(note)

        return note


    def delete_note(self,note_id: int,user_id: int,):
        note = (
        self.db.query(Note)
        .filter(
            Note.id == note_id,
            Note.user_id == user_id,
        )
        .first())

        if not note:
            return False

        self.db.delete(note)
        self.db.commit()

        return True