from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

class Image(Base):
    __tablename__ = "images"
    label = mapped_column(String(64), primary_key=True, unique=True)
    discord_url = mapped_column(String(255))

    def __repr__(self) -> str:
        return f"Images(label={self.label!r}, discord_url={self.discord_url!r})"

class Card(Base):
    __tablename__ = "cards"
    id = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    card_style: Mapped[str] = mapped_column(String(32))
    title: Mapped[str] = mapped_column(String(32))
    attribute: Mapped[str] = mapped_column(String(32))
    level: Mapped[str] = mapped_column(String(32))
    type: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(String(255))
    atk: Mapped[str] = mapped_column(String(32))
    defe: Mapped[str] = mapped_column(String(32))
    cost: Mapped[int] 
    image_label: Mapped[str] = mapped_column(String(64), ForeignKey("images.label"))
    image: Mapped["Image"] = relationship()
    shoppable: Mapped[bool] = mapped_column()

    def __repr__(self) -> str:
        return f"Card(title={self.title!r})"

# ... (other models remain unchanged)