from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.note import NoteCreate, NoteResponse,NoteUpdate
from app.services.note_service import NoteService
from app.core.security import get_current_user
from app.models.user import User
from uuid import UUID
router = APIRouter(prefix="/papers",tags=["Notes"],)
@router.post("/{paper_id}/notes",response_model=NoteResponse,)
def note(note_data:NoteCreate,paper_id:UUID,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    service = NoteService(db)
    note = service.create_note(
    user_id=current_user.id,
    paper_id=paper_id,
    content=note_data.content)
    if not note:
        raise HTTPException(status_code=404,detail="Paper not found",)
    return note
@router.get(
    "/{paper_id}/notes",
    response_model=list[NoteResponse],
)
def get_notes(
    paper_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = NoteService(db)

    return service.get_notes_for_paper(
        paper_id=paper_id,
        user_id=current_user.id,
    )
@router.put(
    "/notes/{note_id}",
    response_model=NoteResponse,
)
def update_note(
    note_data: NoteUpdate,
    note_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = NoteService(db)

    note = service.update_note(
        note_id=note_id,
        user_id=current_user.id,
        content=note_data.content,
    )

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found",
        )

    return note

@router.delete("/notes/{note_id}", status_code=204)
def delete_note(
    note_id:UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = NoteService(db)

    deleted = service.delete_note(
        note_id=note_id,
        user_id=current_user.id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Note not found",
        )