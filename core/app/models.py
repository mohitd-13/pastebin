from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, func, text

from app.database import Base


class Bin(Base):
    __tablename__= "bins"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Timestamp with server default
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    
    # Expiry time default to creation time + 3 months
    expiry_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("now() + interval '3 months'"),
        index=True
    )
