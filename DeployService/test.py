import os

import boto3
from dotenv import load_dotenv

load_dotenv()
s3_client = boto3.client('s3',aws_access_key_id= os.getenv('AWS_ACCESS_KEY_ID'),aws_secret_access_key= os.getenv('AWS_SECRET_ACCESS_KEY'))
bucket = os.getenv('BUCKET_NAME')

prefix = '/'
result = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix,  Delimiter='/')
for o in result.get('CommonPrefixes'):
    print(o.get('Prefix'))