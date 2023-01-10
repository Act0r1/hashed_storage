import os
import hashlib
import os

from sql_app import auth
from fastapi import UploadFile, Depends
from sql_app.models import User


BLOCK_SIZE = 65536


async def create_working_dir(
    file: UploadFile, user: User = Depends(auth.get_current_active_user)
):
    file_hash = hashlib.sha256()
    cwd = os.getcwd()

    # creating dir files
    if not os.path.isdir(f"{cwd}/files"):
        os.makedirs(f"{cwd}/files")
    # creating dir with username if this one doesn't exist
    if not os.path.isdir(f"{cwd}/files/{user.username}"):
        os.makedirs(f"{cwd}/files/{user.username}")

    # creating file in dir
    with open(f"{cwd}/files/{user.username}/{file.filename}", "wb") as f:
        f.write(await file.read())

    # hashing content
    with open(f"{cwd}/files/{user.username}/{file.filename}", "rb") as f:
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
