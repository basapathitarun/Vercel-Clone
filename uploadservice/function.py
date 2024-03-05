import random
import string
import os

import boto3

from dotenv import load_dotenv

# generating id for user
def generate()->str:
    substr = string.ascii_lowercase+string.ascii_uppercase+string.digits
    id = ""
    length = 5
    for i in range(length):
        id+= random.choice(substr)
    return id


def getAllfiles(directoryname)->list:
    Allfiles = []

    for dirpath,dirname,filenames in os.walk(directoryname):
        for file in filenames:
            exitingfilename = os.path.join(dirpath,file)
            Allfiles.append(exitingfilename)

    return Allfiles

def uploadAllfiles(Allfilename):
    load_dotenv()
    s3 = boto3.client("s3",aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    for file in Allfilename:
        cur_dircetory = os.getcwd()
        cur_dircetory_len = len(cur_dircetory)
        cur_dircetory_len+= len("vercel\\")
        s3_key = file[cur_dircetory_len:]
        s3_key = s3_key.replace('\\','/')
        s3_key = s3_key[1:]
        s3.upload_file(file,os.getenv('BUCKET_NAME'),s3_key)
