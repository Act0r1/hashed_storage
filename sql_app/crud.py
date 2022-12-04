from sqlalchemy.orm import Session
from . import schema
from . import models
from sqlalchemy.orm import Session
from . import auth 



def create_user(db:Session,user:schema.UserCreate):
    hash_passw = auth.get_password_hash(user.password) 
    db_user = models.User(username=user.username, hashed_password=hash_passw)
    # we don't return password hash back to front
    user.dict().pop('password')
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return user
   
def return_user(db:Session, username:str):
    return db.query(models.User).filter(models.User.username == username).first()

