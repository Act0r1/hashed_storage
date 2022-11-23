from fastapi import FastAPI, Query, Path
from pydantic import BaseModel
from typing import List

app = FastAPI()

@app.get("/")
async def root():
    return {"message:":"Hello world"}
