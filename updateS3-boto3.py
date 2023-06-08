import boto3
from botocore.exceptions import NoCredentialsError

def delete_file(bucket_name, object_name):
    s3 = boto3.client('s3')
    try:
        s3.delete_object(Bucket=bucket_name, Key=object_name)
        print(f'Successfully deleted {object_name} from {bucket_name}')
    except NoCredentialsError:
        print("No credentials found")

def upload_file(bucket_name, file_name, object_name=None):
    if object_name is None:
        object_name = file_name
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket_name, object_name)
        print(f'Successfully uploaded {file_name} to {bucket_name}')
    except NoCredentialsError:
        print("No credentials found")

# set these variables before running the program
bucketName = 'twitterbot-shalen-dev'  # replace with your bucket name
objectName = 'data.txt'  # replace with your S3 object name
fileName = 'data.txt'  # replace with your local file name

delete_file(bucketName, objectName)
upload_file(bucketName, fileName, objectName)
