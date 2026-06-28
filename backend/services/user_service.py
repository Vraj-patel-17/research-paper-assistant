from app.models.user import User
def create_user(db,username,email,password):
    user=User(username=username,email=email,hashed_password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_email(db,email):
    return ( db.query(User).filter(User.email==email).first())

def update_username(db,email,new_username):
    user=get_user_by_email(db,email)
    if user:
        user.username=new_username
        db.commit()
        db.refresh(user)
        return user

def delete_user(db,email):
    user=get_user_by_email(db,email)
    if user:
        db.delete(user)
        db.commit()
    return user