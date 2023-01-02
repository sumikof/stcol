import re

import boto3
from logging import getLogger

import data_connector
import db.model
from settings import config, secret

import pandas as pd
import re

from data_connector.connector import Connector

logger = getLogger(__name__)


class S3DataManager(Connector):
    def __init__(self, model):
        super().__init__(model)

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

    @property
    def bucket(self):
        return self.s3.Bucket(self.bucket_name)
    def upload_datafile(self, filepath: str, key: str):
        try:
            self.bucket.upload_file(Filename=filepath, Key=key)
            logger.info(f"Finish upload key={key} file={filepath}")
        except Exception as e:
            logger.error(e)

    def upload_dataframe(self, dataframe, key):
        s3_object = self.bucket.Object(key)
        s3_object.put(Body=dataframe.to_csv(None).encode('utf_8'))

    def get_daily_data(self,symbols=None, date=None, count=None):
        pattern_str = f"{self.model.__tablename__}/DAILY_([0-9])+_{self.model.filename}"
        pattern = re.compile(pattern_str)

        return_list = []
        for obj in self.filelist:
            ret = pattern.match(obj.key)
            if ret:
                if ret.group(1) > date:
                    return_list.append(obj.key)

        return return_list

    def get_data(self,key) -> pd.DataFrame:
        from io import StringIO
        try:
            s3_object = self.bucket.Object(key)
            csv_string = s3_object.get()['Body'].read().decode('utf-8')
            return pd.read_csv(StringIO(csv_string), index_col=0)
        except Exception as e:
            logger.error(e)

    @property
    def filelist(self):
        return self.bucket.objects.filter(Prefix=self.model.__tablename__)

def upload_file(model):
    filecom = data_connector.FileConnector(model)
    s3con = S3DataManager(model)
    for file in filecom.searchfile():
        filepath = str(file)
        key = '/'.join([file.parent.name, file.name])
        s3con.upload_datafile(filepath=filepath, key=key)


def insert_data(date):
    from logging import basicConfig, INFO
    basicConfig(level=INFO)

    model = db.model.DomStockRate
    s3con = S3DataManager(model)
    dom_stock_table = data_connector.DBConnector(model)

    pattern_str = f"{model.__tablename__}/DAILY_([0-9]+)_{model.filename}"
    pattern = re.compile(pattern_str)

    rlist = [i.key for i in s3con.filelist if (match := pattern.match(i.key)) and match.group(1) > date]
    for key in rlist:
        df = s3con.get_data(key)
        dom_stock_table.store_data(df)
        logger.info(f'insert data {key}')


if __name__ == '__main__':
    insert_data('yyyymmdd')
