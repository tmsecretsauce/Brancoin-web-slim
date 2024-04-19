
from curses import echo
from dependency_injector import containers, providers

from sqlalchemy import create_engine, true
from sqlalchemy.orm import sessionmaker
from envvars import Env


class DbService():
    def __init__(self, url) -> None:
        self.engine = create_engine(url)
        self.Session = sessionmaker(self.engine)


class DbContainer(containers.DeclarativeContainer):
    service = providers.Singleton(
        DbService,
        url=Env.db_conn_str
    )

