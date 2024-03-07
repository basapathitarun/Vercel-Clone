import boto3
import os
from dotenv import load_dotenv


def downloadFromS3(id):
    load_dotenv()

    # Create an S3 client
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )

    # Specify the bucket name
    bucket_name = os.getenv('BUCKET_NAME')

    # List objects in the bucket
    response = s3.list_objects_v2(Bucket=bucket_name)

    # Check if any object's key starts with the specified path
    if 'Contents' in response:
        for obj in response['Contents']:
            path = f'output/{id}'
            if obj['Key'].startswith(path):
                obj_key = obj['Key']
                obj_key = obj_key.replace('//','\\')
                destination_file_path = os.path.join(os.getcwd(),'DeployService', obj_key)
                destination_file_dir = os.path.dirname(destination_file_path)
                try:
                    os.makedirs(destination_file_dir, exist_ok=True)
                    if not os.path.isdir(destination_file_path):
                        s3.download_file(bucket_name, obj_key, destination_file_path)
                        print(f"Downloaded {obj_key} to {destination_file_path}")
                except Exception as e:
                    print(f"Error downloading {obj_key}: {e}")


def getAllfiles(directoryname)->list:
    Allfiles = []

    for dirpath,dirname,filenames in os.walk(directoryname):
        for file in filenames:
            exitingfilename = os.path.join(dirpath,file)
            Allfiles.append(exitingfilename)

    return Allfiles

def uploadS3(id):
    directoryname = os.path.join(os.getcwd(),'DeployService','Build',f'{id}')
    Allfilename = getAllfiles(directoryname)
    print(Allfilename)
    load_dotenv()
    s3 = boto3.client("s3", aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                      aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    for file in Allfilename:
        cur_dircetory = os.getcwd()
        print(cur_dircetory)
        cur_dircetory_len = len(cur_dircetory)
        cur_dircetory_len += len("DeployService/")
        s3_key = file[cur_dircetory_len:]
        s3_key = s3_key.replace('\\', '/')
        print(f's3_key-> {s3_key}')
        s3_key = s3_key[1:]
        print(file)
        s3.upload_file(file, os.getenv('BUCKET_NAME'), s3_key)

    print('Build dir uploaded to S3 ')



