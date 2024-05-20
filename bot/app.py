from datetime import datetime
from threading import Thread
from sqlalchemy import create_engine, select
from models.dbcontainer import DbContainer, DbService
from dependency_injector.wiring import Provide, inject
from envvars import Env
import webserver
import webserver.web


container2 = DbContainer()
container2.init_resources()
container2.wire(modules=[__name__, webserver.web])


web_server_thread = Thread(target = webserver.web.start)
web_server_thread.start()
web_server_thread.join()