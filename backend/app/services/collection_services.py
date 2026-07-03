from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.models.collection import Collection
from app.schemas.collection import CollectionCreate

def create_collection(db: Session,user_id: int,collection_data: CollectionCreate,) -> Collection:
    collection = Collection(name=collection_data.name,description=collection_data.description,user_id=user_id,)

    db.add(collection)
    try:
        db.commit()
        db.refresh(collection)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A collection with this name already exists.",
        )
    return collection

def get_user_collections(db: Session,user_id: int,) -> list[Collection]:
    return (db.query(Collection).filter(Collection.user_id == user_id).all())

def get_collection_by_id(db: Session,collection_id: int,user_id: int,) -> Collection:
    collection = (db.query(Collection).filter(Collection.id == collection_id,Collection.user_id == user_id,).first())

    if collection is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Collection not found.",
        )
    return collection

def delete_collection(db: Session,collection_id: int,user_id: int,):
    collection = get_collection_by_id(db,collection_id,user_id,)
    db.delete(collection)
    db.commit()