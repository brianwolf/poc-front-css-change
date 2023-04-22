import os
from datetime import datetime, timedelta

import boto3

_s3 = None


def config():

    global _s3
    _s3 = boto3.resource('s3',
                         endpoint_url=os.getenv('S3_URL'),
                         aws_access_key_id=os.getenv('S3_ACCESS_KEY'),
                         aws_secret_access_key=os.getenv('S3_SECRET_KEY'),
                         )


def prepare_static_files():

    client = os.getenv("CLIENT")
    bucket = os.getenv("S3_BUCKET")

    global _s3

    client_s3_objects = [
        object
        for object
        in _s3.Bucket(bucket).objects.all()
        if str(object.key).startswith(client)
    ]

    for s3_object in client_s3_objects:
        if _need_update_file(s3_object):
            _download_file(s3_object)


def _need_update_file(s3_object: any) -> bool:

    path = _get_local_path(s3_object)

    if not os.path.exists(path):
        return True

    last_modified_local = datetime.fromtimestamp(os.path.getmtime(path))
    last_modified_s3 = datetime.fromisoformat(
        str(s3_object.last_modified)).replace(tzinfo=None) - timedelta(hours=3)

    if last_modified_s3 > last_modified_local:
        return True

    return False


def _download_file(s3_object: any):

    path = _get_local_path(s3_object)

    if os.path.exists(path):
        os.remove(path)

    os.makedirs(os.path.dirname(path), exist_ok=True)

    bucket = os.getenv("S3_BUCKET")

    global _s3
    _s3.Bucket(bucket).download_file(s3_object.key, path)


def _get_local_path(s3_object: any) -> str:
    file_name = str(s3_object.key).split('/')[1]
    client = _get_client(s3_object)
    return f'static/{client}/{file_name}'


def _get_client(s3_object: any) -> str:
    return str(s3_object.key).split('/')[0]
