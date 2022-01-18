import boto3
from logging import getLogger

import pandas as pd

logger = getLogger(__name__)


class S3DataManager:
    def __init__(self, config):
        self.aws_access_key_id = config['aws_access_key_id']
        self.aws_secret_access_key = config['aws_secret_access_key']
        self.endpoint_url = config['endpoint_url']
        self.bucket_name = config['bucket_name']

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

    def download_datafile(self, key: str):
        from io import StringIO
        try:
            s3_object = self.s3.Bucket(self.bucket_name).Object(key)
            csv_string = s3_object.get()['Body'].read().decode('utf-8')
            return pd.read_csv(StringIO(csv_string))
        except Exception as e:
            logger.error(e)
