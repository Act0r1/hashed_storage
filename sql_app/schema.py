from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class UserInDb(BaseModel):
    username: str


class TokenData(BaseModel):
    username: str


class User(BaseModel):
    id: int | None = None
    username: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    username: str


class File(BaseModel):
    name: str

    class Confing:
        orm_mode = True


class DeleteFile(BaseModel):
    name: str
