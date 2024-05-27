import datetime
from typing import List
from typing import Optional
from sqlalchemy import BLOB, Float, ForeignKey, ForeignKeyConstraint, Integer, LargeBinary, PrimaryKeyConstraint, UniqueConstraint, null, true
from sqlalchemy import String
import sqlalchemy
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from models.base import Base


class Image(Base):
    __tablename__ = "images"
    label = mapped_column(String(32), primary_key=True, unique=True)
    bin = mapped_column(LargeBinary(length=(2**32)-1))

    def __repr__(self) -> str:
        return f"Images(label={self.label!r}"
    
    
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
    image_label: Mapped[str] = mapped_column(String(32), ForeignKey("images.label"))
    image: Mapped["Image"] = relationship()
    shoppable: Mapped[bool] = mapped_column()

    def __repr__(self) -> str:
        return f"Card(title={self.title!r}"
    
class BoosterPack(Base):
    __tablename__ = "booster_pack"
    id = mapped_column(String(32), primary_key=True, unique=True)
    cost: Mapped[int]
    image_label: Mapped[str] = mapped_column(String(32), ForeignKey("images.label"))
    image: Mapped["Image"] = relationship()
    desc: Mapped[str] = mapped_column(String(32))
    booster_segments: Mapped[List["BoosterSegment"]] = relationship()

class BoosterSegment(Base):
    __tablename__ = "booster_segments"
    # id = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    booster_pack_id: Mapped[str] = mapped_column(String(32), ForeignKey("booster_pack.id"),  primary_key=True)
    id = mapped_column(String(32), primary_key=True)
    num_cards_to_draw: Mapped[int]
    booster_cards: Mapped[List["BoosterCard"]] = relationship()
    bg_fname: Mapped[str] = mapped_column(String(32), nullable=True)

    __table_args__ = (
        PrimaryKeyConstraint('booster_pack_id', 'id'),
    )

class BoosterCard(Base):
    __tablename__ = "booster_card"
    id = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    card_id: Mapped[Integer] = mapped_column(ForeignKey("cards.id"))
    booster_pack_id: Mapped[str] = mapped_column(String(32))
    booster_segment_id: Mapped[str] = mapped_column(String(32))
    chance: Mapped[float]
    card: Mapped["Card"] = relationship()

    __table_args__ = (ForeignKeyConstraint(["booster_pack_id", "booster_segment_id"],
                                           ["booster_segments.booster_pack_id", "booster_segments.id"]),
                      {})