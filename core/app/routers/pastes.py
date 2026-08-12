from app.database import get_db
from app.schemas import PasteCreate, PasteResponse

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

router = APIRouter(
    prefix="/pastes",
    tags=["Pastes"],
)

SessionDep = Annotated[AsyncSession, Depends(get_db)]

@router.post("/", status_code=201, response_model=PasteResponse)
async def create_link(text: PasteCreate, db: SessionDep):
    """
    Create a new paste record with the provided content.
    """        
    return


@router.get("/{paste_id}", status_code=200, response_model=PasteResponse)
def get_link(paste_id: str, db: SessionDep):
    """
    Retrieve a paste by its ID.
    """
    # Logic to retrieve a paste by ID goes here
    return {"message": "Paste retrieved successfully", "paste_id": paste_id}


@router.delete("/{paste_id}", status_code=204)
def delete_link(paste_id: str, db: SessionDep):
    """
    Delete a paste by its ID.
    """
    # Logic to delete a paste by ID goes here
    return {"message": "Paste deleted successfully", "paste_id": paste_id}