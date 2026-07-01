from app.models.user import User
from sqlalchemy.orm import Session
from app.core.security import hash_password,verify_password
def create_user(db:Session,username,email,password):
    user=User(username=username,email=email,hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_email(db:Session,email):
    return ( db.query(User).filter(User.email==email).first())

def update_username(db:Session,email,new_username):
    user=get_user_by_email(db,email)
    if user:
        user.username=new_username
        db.commit()
        db.refresh(user)
        return user
    
def delete_user(db:Session,email):
    user=get_user_by_email(db,email)
    if user:
        db.delete(user)
        db.commit()
    return user

def authenticate_user(db:Session,email,password):
    user=get_user_by_email(db,email)
    if not user:
        return None
    if not verify_password(password,user.hashed_password):
        return None
    return user