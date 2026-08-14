from fastapi import APIRouter, HTTPException, Response

from app.dependencies import DBSessionDep, S3SessionDep
from app.schemas import PasteCreate, PasteResponse
from app.service import (
    delete_paste_record,
    insert_new_record_with_retries,
    read_content_from_bucket,
    read_content_metadata,
)

router = APIRouter(
    prefix="/pastes",
    tags=["Pastes"],
)

@router.post("/", status_code=201, response_model=PasteResponse)
async def create_paste(text: PasteCreate, db: DBSessionDep, s3_client: S3SessionDep):
    """
    Create a new paste records.
    """
    result = await insert_new_record_with_retries(text.content, db, s3_client)
    return result

@router.get("/metadata/{paste_id}", status_code=200, response_model=PasteResponse)
async def read_paste_metadata(paste_id: str, db: DBSessionDep):
    """
    Retrieve a paste metadata by its ID.
    """
    metadata = await read_content_metadata(paste_id, db)
    if not metadata:
        raise HTTPException(status_code=404, detail="Paste metadata not found")
    return metadata

@router.get("/{paste_id}", status_code=200)
async def read_paste(paste_id: str, s3_client: S3SessionDep) -> str:
    """
    Retrieve a paste content by its ID.
    """
    content = await read_content_from_bucket(paste_id, s3_client)
    if not content:
        raise HTTPException(status_code=404, detail="Paste Content not found")
    return content

@router.delete("/{paste_id}")
async def delete_paste(paste_id: str, db: DBSessionDep, s3_client: S3SessionDep):
    """
    Delete a paste by its ID.
    """
    deleted = await delete_paste_record(paste_id, db, s3_client)
    if not deleted:
        raise HTTPException(status_code=404, detail="Paste not found")
    return Response(status_code=204)
