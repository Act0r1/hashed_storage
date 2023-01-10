import hashlib
import logging
import os


from datetime import timedelta
from misc.gen_salt import generate_random_salt
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi import UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sql_app import auth
from sql_app.yield_db import get_db
from sql_app.database import Base, engine
from sql_app import schema
from misc.os_stuff import create_working_dir
from misc.zipping_file import zip_file
from sql_app import crud
from sql_app.models import User


BLOCK_SIZE = 65536
app = FastAPI()
templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)


@app.post("/token", response_model=schema.Token)
async def token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    current_user = auth.auth_user(db, form_data.username, form_data.password)
    logging.info("current_user auth")
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": current_user.username}, expire_time=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/", response_class=HTMLResponse)
async def root(req: Request):
    return templates.TemplateResponse("home.html", {"request": req})


@app.post("/signup", response_model=schema.UserOut)
async def singup(*, db: Session = Depends(get_db), user_in: schema.UserCreate):
    current_user = db.query(User).filter(User.username == user_in.username).first()
    if current_user:
        raise HTTPException(
            status_code=400, detail="The current_user with this name already exists"
        )
    salt = generate_random_salt()
    current_user = crud.create_user(db, current_user=user_in, salt=salt)
    current_user = schema.UserOut(**current_user.dict())

    return current_user


@app.post("/login", response_model=schema.Token, response_class=HTMLResponse)
async def login(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    # auth current_user
    current_user = auth.auth_user(
        db, username=form_data.username, password=form_data.password
    )
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    return HTMLResponse(content="<h1>Cool, you logged in</h1>")


@app.post("/uploadfile")
async def uploadfile(
    file: UploadFile,
    current_user: User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db),
):
    file_hash = hashlib.sha256()
    cwd = os.getcwd()
    path = f"{cwd}/files/{current_user.username}/{file.filename}"

    # creating dir files
    if not os.path.isdir(f"{cwd}/files"):
        os.makedirs(f"{cwd}/files")
    # creating dir with username if this one doesn't exist
    if not os.path.isdir(f"{cwd}/files/{current_user.username}"):
        os.makedirs(f"{cwd}/files/{current_user.username}")

    # creating file in dir
    with open(f"{cwd}/files/{current_user.username}/{file.filename}", "wb") as f:
        f.write(await file.read())

    # hashing content
    with open(path, "rb") as f:
        fb = f.read(BLOCK_SIZE)
        while len(fb) > 0:
            file_hash.update(fb)
            fb = f.read(BLOCK_SIZE)
    hash_of_file = file_hash.hexdigest()
    end_path = cwd + f"/store/{hash_of_file[:2]}"
    if not os.path.isdir(end_path) and not os.path.exists(
        end_path + f"/{hash_of_file}"
    ):
        os.makedirs(end_path)

    with open(f"{end_path}/{hash_of_file}", "w"):
        pass


    # zipping file
    zip_file(
        file=UploadFile,
        name=file.filename,
        user=current_user.username,
        cwd=os.getcwd(),
    )
    file_scheme = schema.File(
        name=file.filename, owner=current_user.username, path=path
    )
    # add file to db
    crud.add_file(db, file_scheme)


@app.delete("/delete")
async def delete_file(
    name_of_file: str,
    db: Session = Depends(get_db),
):
    get_path = crud.get_info_about_file(db, name_of_file)
    file = schema.File(name=get_path.name, path=get_path.path, owner=get_path.owner)
    crud.delete_file(db, file)
    os.remove(get_path.path)


@app.get("/users/me/", response_model=schema.UserInDb)
async def read_users_me(current_user: User = Depends(auth.get_current_active_user)):
    return schema.UserInDb(username=str(current_user.username))
