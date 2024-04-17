from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from models.base import Base

class User(Base):
    __tablename__ = "user_account"
    user_id: Mapped[str] = mapped_column(primary_key=True)
    guild_id: Mapped[str] = mapped_column(primary_key=True)
    __table_args__ = (
        PrimaryKeyConstraint('guild_id', 'user_id'),
    )
    
    def __repr__(self) -> str:
        return f"User(id={self.user_id!r}, guild={self.guild_id!r})"
