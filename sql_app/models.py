from sqlalchemy import  Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    hashed_pass = Column(String)

    items = relationship("File", back_populates="owner")

class File(Base):
    __tablename__="files"
    id = Column(Integer, primary_key=True, index=True)
    size = Column(Float)
    owner_id = Column(Integer, ForeignKey("users.id"))

    items = relationship("User", back_populates="files")
