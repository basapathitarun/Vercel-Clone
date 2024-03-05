from django.http import JsonResponse

from .aws import downloadFromS3,uploadS3

def index(request):
    downloadFromS3()

    # convert react files to html css

    # upload build files
    id='4JGgh'
    uploadS3(id)

    return JsonResponse({"id":'id'})
