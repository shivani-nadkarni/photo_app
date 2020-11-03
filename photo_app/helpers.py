"""This establishes connection to minio object storage server.
Specifies upload file method.
"""

import logging
import boto3
from botocore.exceptions import ClientError
from botocore.client import Config
from photo_app import app

# Use S3 object storage
s3_obj = boto3.client('s3',
                      aws_access_key_id=app.config['S3_KEY'],
                      aws_secret_access_key=app.config['S3_SECRET'],
                      config=Config(signature_version='s3v4'))

def upload_file_to_s3(s3_file_path, file, bucket_name):
    """This method is used to upload file to the bucket.

    :param s3_file_path: Gives file path for storage, relative to the bucket
    :param file: File to be stored
    :param bucket_name: The bucket where the file is to be kept
    """
    # Upload the file
    s3_obj.upload_fileobj(
            file,
            bucket_name,
            s3_file_path,
            ExtraArgs={
                'ContentType': file.content_type
            }
    )

def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    try:
        response = s3_obj.generate_presigned_url(
                                        'get_object',
                                        Params={
                                            'Bucket': bucket_name,
                                            'Key': object_name
                                        },
                                        ExpiresIn=expiration)
    except ClientError as exc:
        logging.error(exc)
        return None

    # The response contains the presigned URL
    return response
    
