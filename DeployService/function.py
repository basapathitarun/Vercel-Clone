import asyncio

import redis
from .aws import downloadFromS3,uploadS3
from .build import buildReact
async def gettingID():
    client = redis.Redis(host='localhost',port=6379)
    key, value = client.brpop('build-queue', 0)
    if isinstance(value, bytes):
        value = value.decode('utf-8')
    return value

async def main():
    while True:
        id = await gettingID()
        print(id)
        downloadFromS3(id)
        # Build downloaded files
        buildReact(id)
        uploadS3(id)
        publish = redis.Redis(host='localhost', port=6379)
        publish.hset('status',id,'Deployed')



