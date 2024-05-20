import os

class Env():
    db_host = os.environ['POSTGRES_HOST'] 
    db_password = os.environ['POSTGRES_PASSWORD']
    db_user = os.environ['POSTGRES_USER']
    db_name = os.environ['POSTGRES_DB']
    db_type = os.environ['DB_TYPE']
    
    db_conn_str = f"{db_type}://{db_user}:{db_password}@{db_host}/{db_name}"
    web_port = os.environ['WEB_PORT']