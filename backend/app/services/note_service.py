from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.note import Note
from app.models.paper import Paper
from uuid import UUID

class NoteService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_note(self, user_id: UUID, paper_id: UUID, content: str):
        paper = await self.db.get(Paper, paper_id)
        if not paper:
            return None
        note = Note(content=content, user_id=user_id, paper_id=paper_id)
        self.db.add(note)
        await self.db.commit()
        await self.db.refresh(note)
        return note

    async def get_notes_for_paper(self, paper_id: UUID, user_id: UUID):
        result = await self.db.execute(
            select(Note)
            .where(Note.paper_id == paper_id, Note.user_id == user_id)
            .order_by(Note.updated_at.desc())
        )
        return result.scalars().all()

    async def update_note(self, note_id: UUID, user_id: UUID, content: str):
        result = await self.db.execute(
            select(Note).where(Note.id == note_id, Note.user_id == user_id)
        )
        note = result.scalar_one_or_none()
        if not note:
            return None

        note.content = content

        await self.db.commit()
        await self.db.refresh(note)

        return note

    async def delete_note(self, note_id: UUID, user_id: UUID):
        result = await self.db.execute(
            select(Note).where(Note.id == note_id, Note.user_id == user_id)
        )
        note = result.scalar_one_or_none()

        if not note:
            return False

        await self.db.delete(note)
        await self.db.commit()

        return True