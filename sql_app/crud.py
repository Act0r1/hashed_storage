from sqlalchemy.orm import Session
from sqlalchemy import delete
from . import schema
from . import models
from . import auth


def create_user(db: Session, user: schema.UserCreate, salt: str):
    hash_passw = auth.get_password_hash(user.password + salt)
    db_user = models.User(username=user.username, hashed_password=hash_passw, salt=salt)
    # we don't return password hash back to front
    user.dict().pop("password")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return user


def return_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def add_file(db: Session, file: schema.File):
    db_file = models.File(name=file.name, path=file.path, owner=file.owner)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)


def delete_file(db: Session, file: schema.File):
    db_path = db.query(models.File).where(models.File.name == file.name).first()
    db.delete(db_path)
    db.commit()


def get_info_about_file(db: Session, name_of_file: str) -> schema.File:
    return db.query(models.File).filter(models.File.name == name_of_file).first()
