import hashlib
from misc.gen_salt import generate_random_salt
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi import  UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sql_app import auth
from sql_app.database import Base, engine, SessionLocal
from sql_app import schema
from sql_app import crud
from sql_app.models import User



app = FastAPI()
templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# @app.post("/token", response_model=schema.Token)
# async def token(db:Session=Depends(get_db),form_data:OAuth2PasswordRequestForm=Depends()):
#     user = auth.auth_user(db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = auth.generate_token(
#         data={"sub": user.username}, expire_time=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}


@app.get("/", response_class=HTMLResponse)
async def root(req: Request):
    return templates.TemplateResponse("home.html", {"request": req})


@app.post("/signup", response_model=schema.UserOut)
async def singup(*, db: Session = Depends(get_db), user_in: schema.UserCreate):
    user = db.query(User).filter(User.username == user_in.username).first()
    if user:
        raise HTTPException(
            status_code=400, detail="The user with this name already exists"
        )
    salt = generate_random_salt()
    user = crud.create_user(db, user=user_in, salt=salt)
    user = schema.UserOut(**user.dict())

    return user


@app.post("/login", response_model=schema.Token, response_class=HTMLResponse)
async def login(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = auth.auth_user(db, username=form_data.username, password=form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    return HTMLResponse(content="<h1>Cool, you logged in</h1>")


@app.post("/uploadfile")
async def uploadfile(file: UploadFile):
    asd = file.file.read()
    # hashing name
    with open("asd.pdf", "wb") as f:
        f.write(asd)

    with open("asd.pdf", "rb") as f:
        grr = hashlib.file_digest(f, "sha256")
        print("hash of file ->", grr)



@app.get("/users/me/", response_model=schema.UserInDb)
async def read_users_me(current_user: User = Depends(auth.get_current_active_user)):
    return current_user


# @app.post("/uploadfile/",response_class=HTMLResponse)
# async def create_upload_file(request: Request):
#     return templates.TemplateResponse("index.html", {"request":request})
