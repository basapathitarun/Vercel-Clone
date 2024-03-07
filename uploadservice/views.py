import os.path


from django.http import JsonResponse
from git import Repo
import redis

from .function import (generate, getAllfiles, uploadAllfiles)

github_url = '''https://github.com/hkirat/react-boilerplate.git'''

def index(request):
    # genearting id
    id = generate()

    # getting absoulute path
    current_file_directory = os.path.join(os.getcwd(),'uploadservice','output')
    file_directory = os.path.join(current_file_directory,id)

    # cloneing the input Github link
    Repo.clone_from(github_url,file_directory)
    # Getting All Cloned Github files and direciory names
    Allfilename = getAllfiles(file_directory)

    # Upload All CLoned files to S3 bucket
    uploadAllfiles(Allfilename)

    # Pushing ID to Redis Queue
    client = redis.Redis(host='localhost',port=6379)
    client.lpush("build-queue",id)
    client.hset('status',id,'Uploaded')
    data = {'id':id,'val': Allfilename}
    return JsonResponse(data)


def status(request):
    id = "lSCdc"
    client = redis.Redis(host='localhost', port=6379)
    status = client.hget('status', id)
    if isinstance(status,bytes):
        status = status.decode('utf-8')
    return JsonResponse({'status': status})








