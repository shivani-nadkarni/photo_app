"""This establishes connection to minio object storage server.
Specifies upload file method.
"""

import boto3
from photo_app import app

def upload_file_to_s3(s3_file_path, file, bucket_name):
    """This method is used to upload file to the bucket.

    :param s3_file_path: Gives file path for storage, relative to the bucket
    :param file: File to be stored
    :param bucket_name: The bucket where the file is to be kept
    """

    # Use S3 object storage
    s3_obj = boto3.client('s3',
                          aws_access_key_id=app.config['S3_KEY'],
                          aws_secret_access_key=app.config['S3_SECRET'])

    # Upload the file
    s3_obj.upload_fileobj(
            file,
            bucket_name,
            s3_file_path,
            ExtraArgs={
                'ACL': 'public-read',
                'ContentType': file.content_type
            }
    )
    