from sqlalchemy import  Column,ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    #salt = Column(String)
    files = relationship("File", back_populates="owner")

class File(Base):
    __tablename__="files"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    # path = Column(String, index=True)
    owner = relationship("User", back_populates="files")
    # optional, maybe don't use
    def __repr__(self) -> str:
        return "File name %s" % self.name
