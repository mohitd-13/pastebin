from datetime import datetime
from pydantic import BaseModel

class PasteCreate(BaseModel):
    content: str
    
    
class PasteResponse(BaseModel):
    id: str
    created_at: datetime
    expiry_at: datetime
    size_bytes: int
