import os
import boto3
import asyncio
from django.http import HttpResponse, JsonResponse
from .aws import downloadFromS3,uploadS3
from .function import main
from dotenv import load_dotenv
def index(request):
    asyncio.run(main())
    return JsonResponse({"id":'id'})

def deploy(request):
    load_dotenv()
    bucket_name = os.getenv('BUCKET_NAME')

    id = '4JGgh'  # Assuming subdomain represents the ID

    # Construct S3 key
    file_path ='index.html'
    key = f'Build/{id}/{file_path}'  # Adjust path as needed

    # Retrieve content from S3
    s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        content = response['Body'].read()
    except s3_client.exceptions.NoSuchKey:
        return HttpResponse(status=404)

    # Determine content type based on file extension
    content_type = 'text/html'  # Default to HTML
    if key.endswith('.css'):
        content_type = 'text/css'
    elif key.endswith('.js'):
        content_type = 'application/javascript'

    # Add content-type header and return content
    return HttpResponse(content, content_type=content_type)