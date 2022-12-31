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

DATABASE = '{0[dbtype]}://{0[user]}:{0[password]}@{0[hostname]}:{0[dbport]}/{0[db_name]}'.format(config["db"])

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


