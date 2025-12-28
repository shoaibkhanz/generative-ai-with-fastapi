import os
from pathlib import Path

import aiofiles
from aiofiles.os import makedirs
from fastapi import UploadFile

DEFAULT_CHUNK_SIZE = 1024 * 1024 * 50  # 50 Mbs


async def save_file(file: UploadFile) -> str:
    await makedirs("uploads", exist_ok=True)
    filepath = str(Path(file.filename).name)
    async with aiofiles.open(filepath, "wb") as f:
        while chunk := await file.read(DEFAULT_CHUNK_SIZE):
            await f.write(chunk)
    return filepath
