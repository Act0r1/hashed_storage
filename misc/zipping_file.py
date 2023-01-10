import os
import zipfile
from fastapi import UploadFile


async def zip_file(file: UploadFile, name: str, user: str, cwd: str) -> None:
    if not os.path.isdir(f"{cwd}/files/{user}/archive_files"):
        os.makedirs(f"{cwd}/files/{user}/archive_files")
    # we find . and after that replacing it with zip
    index = name.find(".")
    with zipfile.ZipFile(
        f"{cwd}/files/{user}/archive_files/{name[:index]}.zip", mode="w"
    ) as zp:
        zp.write(await file.read())
