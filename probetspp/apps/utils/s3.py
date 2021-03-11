from os import path, mkdir
import logging
import boto3
from typing import Optional, Union
from botocore.exceptions import ClientError

from apps.utils.constants import DIR, SUBDIR, BUCKET_FILES

logger = logging.getLogger(__name__)


def upload_file(
    *,
    source: str,
    destination: Optional[str] = None,
    bucket_name: Optional[str] = BUCKET_FILES,
) -> bool:
    """
    Upload a file to an S3 bucket
    :param source: File to upload
    :param destination: S3 object name. If not specified then file_name is used
    :param bucket_name: Bucket to upload to
    :return: True if file was uploaded, else False
    """
    if destination is None:
        destination = source
    s3 = boto3.resource('s3')
    try:
        s3.Bucket(bucket_name).upload_file(source, destination)
    except ClientError as e:
        logger.error(e)
        return False
    return True


def download_file(
    *,
    key: str,
    bucket_name: Optional[str] = BUCKET_FILES
) -> Union[str, None]:
    """
    download file from bucket
    :param bucket_name: bucket name
    :param key: The name of the key to download from.
    :return: path
    """
    local_path = f'{DIR}/{SUBDIR}'
    if not path.exists(local_path):
        mkdir(local_path)
    filename = path.basename(key)
    destination = f'{local_path}/{filename}'
    try:
        s3 = boto3.resource('s3')
        s3.Bucket(bucket_name).download_file(key, destination)
        return destination
    except Exception as e:
        logger.error(e)
