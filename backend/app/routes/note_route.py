from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.note import NoteCreate, NoteResponse
from app.services.note_service import NoteService
from app.core.security import get_current_user
from app.models.user import User
router = APIRouter(prefix="/papers",tags=["Notes"],)
@router.post("/{paper_id}/notes",response_model=NoteResponse,)
def note(paper_id:int,note_data:NoteCreate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    service = NoteService(db)
    note = service.create_note(
    user_id=current_user.id,
    paper_id=paper_id,
    content=note_data.content)
    if not note:
        raise HTTPException(status_code=404,detail="Paper not found",)
    return note
    