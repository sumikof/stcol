import os
import yaml


TOP_DIR = os.path.dirname(__file__)
ENVIRONMENT = os.getenv('ENVIRONMENT', default='dev')
with open(os.path.join(TOP_DIR, 'config', f'secret.yaml')) as yaml_file:
    boto3_config = yaml.safe_load(yaml_file)

with open(os.path.join(TOP_DIR, 'config', f'config_{ENVIRONMENT}.yaml')) as yaml_file:
    config = yaml.safe_load(yaml_file)

DATA_PATH = os.path.join(TOP_DIR, "data")
FUTURE_DATA = "future.dat"
INDEX_DATA = "index.dat"
OVR_ETF_DATA = "ovr_etf.dat"
BOND_YIELDS_DATA = "bond_yields.dat"
EXCHANGE_RATE_DATA = 'exchange_rate'
DOM_STOCK_DATA = 'dom_stock'

ADJUST_CLOSE = 'AdjClose'
