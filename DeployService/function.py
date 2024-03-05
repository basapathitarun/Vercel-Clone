import asyncio
import redis

async def gettingID():
    client = redis.Redis(host='localhost',port=6379)
    listOfId = []
    while True:
        key,value=client.brpop('build-queue',0)

        if isinstance(value,bytes):
            value=value.decode('utf-8')

        print(value)
        listOfId.append(value)
        await asyncio.sleep(0)
        return listOfId

async def main():
    listOfId = await gettingID()
    print(listOfId)


asyncio.run(main())


