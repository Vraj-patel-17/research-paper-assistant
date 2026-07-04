from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.models.collection import Collection
from app.schemas.collection import CollectionCreate
from sqlalchemy import select
from app.models.paper import Paper
from app.models.collection_paper import CollectionPaper
from app.schemas.collection_paper import AddPaperToCollection

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

def add_paper_to_collection(
    db:Session,
    collection_id:int,
    user_id:int,
    data:AddPaperToCollection
):
    collection=get_collection_by_id(db,collection_id,user_id)
    paper=db.get(Paper,data.paper_id)
    if not paper:
        raise HTTPException(status_code=404,detail="Paper not found")
    exists=db.scalar(
        select(CollectionPaper).where(
            CollectionPaper.collection_id==collection.id,
            CollectionPaper.paper_id==data.paper_id
        )
    )
    if exists:
        raise HTTPException(status_code=409,detail="Paper already exists in collection")

    collection_paper=CollectionPaper(
        collection_id=collection.id,
        paper_id=data.paper_id
    )
    db.add(collection_paper)
    db.commit()
def get_collection_papers(
    db:Session,
    collection_id:int,
    user_id:int
):
    get_collection_by_id(db,collection_id,user_id)

    papers=db.scalars(
        select(Paper)
        .join(CollectionPaper)
        .where(CollectionPaper.collection_id==collection_id)
    ).all()

    return papers

def remove_paper_from_collection(
    db:Session,
    collection_id:int,
    paper_id:int,
    user_id:int
):
    get_collection_by_id(db,collection_id,user_id)

    collection_paper=db.scalar(
        select(CollectionPaper).where(
            CollectionPaper.collection_id==collection_id,
            CollectionPaper.paper_id==paper_id
        )
    )

    if not collection_paper:
        raise HTTPException(status_code=404,detail="Paper not found in collection")

    db.delete(collection_paper)
    db.commit()