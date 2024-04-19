from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, UniqueConstraint, true
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from models.base import Base

class User(Base):
    __tablename__ = "user_account"
    id = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id: Mapped[str]
    guild_id: Mapped[str]
    brancoins  = mapped_column(Integer, server_default="10")

    league_user: Mapped["LeagueUser"] = relationship(back_populates="discord_user")

    __table_args__ = (
        UniqueConstraint('user_id', 'guild_id', name='user_guild_uc'),
    )
    
    def __repr__(self) -> str:
        return f"User(id={self.user_id!r}, guild={self.guild_id!r})"

class LeagueUser(Base):
    __tablename__ = "league_user"
    id = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    summoner_name: Mapped[str] = mapped_column(primary_key=true)
    region: Mapped[str] = mapped_column(primary_key=true)
    trackable: Mapped[bool]
    voteable: Mapped[bool]
    
    discord_user_id = mapped_column(Integer, ForeignKey("user_account.id"))
    discord_user: Mapped["User"] = relationship(back_populates="league_user")

    def __repr__(self) -> str:
        return f"region(id={self.region!r}, summoner_name={self.summoner_name!r}, trackable={self.trackable!r}, voteable={self.voteable!r})"
    
class Match(Base):
    __tablename__ = "match"
    match_id: Mapped[str] = mapped_column(primary_key=true)
    processed: Mapped[bool] = mapped_column(server_default="False")

class Votes(Base):
    __tablename__ = "votes"
    id = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    voter: Mapped[str] = mapped_column(ForeignKey("user_account.id"))
    target_league_player: Mapped[str] = mapped_column(ForeignKey("league_user.id"))
    type_of_vote: Mapped[str]
