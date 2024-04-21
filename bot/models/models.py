import datetime
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, ForeignKeyConstraint, Integer, PrimaryKeyConstraint, UniqueConstraint, null, true
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
    summoner_name: Mapped[str]
    tag: Mapped[str]
    trackable: Mapped[bool]
    voteable: Mapped[bool]
    
    discord_user_id = mapped_column(Integer, ForeignKey("user_account.id"))
    discord_user: Mapped["User"] = relationship(back_populates="league_user")

    def __repr__(self) -> str:
        return f"tag(id={self.tag!r}, summoner_name={self.summoner_name!r}, trackable={self.trackable!r}, voteable={self.voteable!r})"
    
class Match(Base):
    __tablename__ = "match"
    match_id: Mapped[str] = mapped_column(primary_key=true)
    finished: Mapped[bool] = mapped_column(server_default="False")
    start_time: Mapped[datetime.datetime] 

    match_players: Mapped[List["MatchPlayer"]] = relationship(back_populates="match")

class MatchPlayer(Base):
    __tablename__ = "match_player"
    match_id: Mapped[str] = mapped_column(ForeignKey("match.match_id"), primary_key=True)
    league_user_id: Mapped[Integer] = mapped_column(ForeignKey("league_user.id"), primary_key=True)
    champion: Mapped[str]

    league_user: Mapped["LeagueUser"] = relationship()
    match: Mapped["Match"] = relationship()

    __table_args__ = (
        PrimaryKeyConstraint('match_id', 'league_user_id'),
    )


class Jackpot(Base):
    __tablename__ = "jackpot"
    guild_id: Mapped[str] = mapped_column(primary_key=True, unique=True)
    brancoins = mapped_column(Integer, server_default="10")

    def __repr__(self) -> str:
        return f"Jackpot(guild_id={self.guild_id!r}, brancoins={self.brancoins!r})"

class Votes(Base):
    __tablename__ = "votes"
    id = mapped_column(Integer, primary_key=True, autoincrement=True, unique=True)
    voter: Mapped[str] = mapped_column(ForeignKey("user_account.id"))
    target_league_player: Mapped[str] = mapped_column(ForeignKey("league_user.id"))
    type_of_vote: Mapped[str]
