from typing import Annotated

from fastapi import FastAPI, File, HTTPException, UploadFile, status

from rag.upload import save_file

app = FastAPI()


@app.post("/upload")
async def file_upload_controller(
    file: Annotated[UploadFile, File(description="Uploaded pdf file description")],
):
    if file.content_type != "pdf":
        HTTPException(
            detail="only pdf file supporeted", status_code=status.HTTP_400_BAD_REQUEST
        )

    try:
        await save_file(file=file)

    except Exception as e:
        HTTPException(
            f"An error occured while saving the file with error: {e}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return {"filename": file.filename, "message": "File uploaded successfully"}
