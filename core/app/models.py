from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    DateTime, func, text, String, Index, Integer
)

from app.database import Base


class Bin(Base):
    __tablename__= "bins"
    
    id: Mapped[str] = mapped_column(String(8), primary_key=True)
    
    # Timestamp with server default
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    
    # Expiry time default to creation time + 3 months
    expiry_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("now() + interval '3 months'"),
    )
    
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = ( 
        # for cleanup jobs
        Index("idx_bins_expiry_at", "expiry_at"),
    )