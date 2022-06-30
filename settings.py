import os
import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from db import model

LOG_FORMAT = '%(asctime)s : %(levelname)s - %(filename)s - %(message)s'

TOP_DIR = os.path.dirname(__file__)
ENVIRONMENT = os.getenv('ENVIRONMENT', default='dev')

with open(os.path.join(TOP_DIR, 'config', f'config_{ENVIRONMENT}.yaml')) as yaml_file:
    config = yaml.safe_load(yaml_file)

with open(os.path.join(TOP_DIR, 'config', f'secret.yaml')) as yaml_file:
    secret = yaml.safe_load(yaml_file)

DATA_PATH = os.path.join(TOP_DIR, "data")

DATABASE = 'mysql+pymysql://{}:{}@{}:3306/{}?charset=utf8'.format(
    config["db"]["user"],
    config["db"]["password"],
    config["db"]["hostname"],
    config["db"]["db_name"]
)
Engine = create_engine(
    DATABASE,
    encoding="utf-8",
    echo=False
)
make_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=Engine
    )
)

FUTURE_DATA = model.FutureRate()
INDEX_DATA = model.IndexRate()
OVR_ETF_DATA = model.OvrEtfRate()
BOND_YIELDS_DATA = model.BondYieldsRate()
EXCHANGE_RATE_DATA = model.ExchangeRate()
DOM_STOCK_DATA = model.DomStockRate()
