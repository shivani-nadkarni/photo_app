""" this establishes connection to minio object storage server,
    specifies upload function to upload images """

import boto3
from photo_app.routes import app

# this is used to upload file to bucket
def upload_file_to_s3(s3_file_path, file, bucket_name):
    s3_obj = boto3.client('s3',
                        endpoint_url=app.config['S3_URL'],
                        aws_access_key_id=app.config['S3_KEY'],
                        aws_secret_access_key=app.config['S3_SECRET'])

    s3_obj.upload_fileobj(
            file,
            bucket_name,
            s3_file_path,
            ExtraArgs={
                'ACL': 'public-read',
                'ContentType': file.content_type
            }
    )
    