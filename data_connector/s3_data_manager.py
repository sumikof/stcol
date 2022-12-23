import boto3
from logging import getLogger
from settings import config, secret

import pandas as pd

from data_connector.connector import Connector

logger = getLogger(__name__)


class S3DataManager(Connector):
    def __init__(self):
        self.aws_access_key_id = secret['aws_access_key_id']
        self.aws_secret_access_key = secret['aws_secret_access_key']
        self.endpoint_url = config['boto3']['endpoint_url']
        self.bucket_name = config['boto3']['bucket_name']

        self.s3 = boto3.resource(
            's3',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            endpoint_url=self.endpoint_url
        )

    def upload_datafile(self, filepath: str, key: str):
        try:
            self.s3.Bucket(self.bucket_name).upload_file(Filename=filepath, Key=key)
            logger.info(f"Finish upload key={key} file={filepath}")
        except Exception as e:
            logger.error(e)

    def upload_dataframe(self, dataframe, key):
        s3_object = self.s3.Bucket(self.bucket_name).Object(key)
        s3_object.put(Body=dataframe.to_csv(None).encode('utf_8'))

    def get_daily_data(self, model, symbols=None):
        from io import StringIO
        try:
            s3_object = self.s3.Bucket(self.bucket_name).Object(model.filename)
            csv_string = s3_object.get()['Body'].read().decode('utf-8')
            return pd.read_csv(StringIO(csv_string), index_col=0)
        except Exception as e:
            logger.error(e)
