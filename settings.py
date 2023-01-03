import os
import yaml
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

LOG_FORMAT = '%(asctime)s : %(levelname)s - %(filename)s - %(message)s'

TOP_DIR = os.path.dirname(__file__)
ENVIRONMENT = os.getenv('ENVIRONMENT', default='dev')

with open(os.path.join(TOP_DIR, 'config', f'config_{ENVIRONMENT}.yaml')) as yaml_file:
    config = yaml.safe_load(yaml_file)

with open(os.path.join(TOP_DIR, 'config', f'secret.yaml')) as yaml_file:
    secret = yaml.safe_load(yaml_file)

DATA_PATH = os.path.join(TOP_DIR, "data")

DATABASE = (
    f'{config["db"]["dbtype"]}://{config["db"]["user"]}:{secret["db"]["password"]}@{config["db"]["hostname"]}'
    f':{config["db"]["dbport"]}/{config["db"]["db_name"]}'
)

Engine = create_engine(
    DATABASE,
    encoding="utf-8",
    echo=False
)
session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=Engine
    )
)
Base = declarative_base()
Base.query = session.query_property()


