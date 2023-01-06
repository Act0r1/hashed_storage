from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from environs import Env

env = Env()
env.read_env()
SQLALCHEMY_DATABASE_URL = env.str("SQLALCHEMY_DATABASE_URL")
engine = create_engine(str(SQLALCHEMY_DATABASE_URL))


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
