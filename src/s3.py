import logging
import re

import boto3
import botocore

logging.getLogger('botocore').setLevel(logging.ERROR)
logging.getLogger('s3transfer').setLevel(logging.ERROR)
logging.getLogger('urllib3').setLevel(logging.ERROR)
logging.getLogger('boto3').setLevel(logging.ERROR)
logging.getLogger('asyncio').setLevel(logging.ERROR)
logging.getLogger('aiobotocore').setLevel(logging.ERROR)
logging.getLogger('s3fs').setLevel(logging.ERROR)

logging.config.fileConfig('config/logging/local.conf')
logger = logging.getLogger(__name__)


def parse_s3(s3path):
    """Split a full S3 file path into S3 bucket path and S3 path.

    Args:
        s3 path (str): full S3 file path

    Returns:
        tuple(s3bucket, s3path) (str, str): path to S3 bucket, path to S3
    """
    regex = r's3://([\w._-]+)/([\w./_-]+)'

    m = re.match(regex, s3path)
    s3bucket = m.group(1)
    s3path = m.group(2)

    return s3bucket, s3path


def upload_file_to_s3(local_path, s3path):
    """Uploads a file from local to the specified S3 path.

    Args:
        local_path (str): local path to the file
        s3path (str): path to the S3 destination

    Returns:
        None
    """
    s3bucket, s3_just_path = parse_s3(s3path)

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(s3bucket)

    try:
        logger.debug('Uploading data to S3.')
        bucket.upload_file(local_path, s3_just_path)
    except botocore.exceptions.NoCredentialsError:
        logger.error('Please provide AWS credentials via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY env variables.')
    else:
        logger.info('Data uploaded from %s to %s', local_path, s3path)
