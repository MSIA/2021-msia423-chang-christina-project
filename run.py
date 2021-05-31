import argparse
import logging.config

from config.flaskconfig import SQLALCHEMY_DATABASE_URI
from src.create_db import create_db
from src.s3 import upload_file_to_s3, download_file_from_s3

logging.config.fileConfig('config/logging/local.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

if __name__ == '__main__':

    # Create parser
    parser = argparse.ArgumentParser(description='Create database or upload data to S3')
    subparsers = parser.add_subparsers(dest='subparser_name')

    # Sub-parser for uploading data to S3 bucket
    sb_s3_upload = subparsers.add_parser('s3_upload', description='Upload data to S3')
    sb_s3_upload.add_argument('--s3path', required=True, help='Where to load data to in S3')
    sb_s3_upload.add_argument('--local_path', default='./data/raw/national-park-trails.csv',
                              help='Where data exists in local')

    # sub-parser for download data to S3 bucket
    sb_s3_download = subparsers.add_parser('s3_download', description='Download data from S3')
    sb_s3_download.add_argument('--local_path', required=True, help='Where to download in local')
    sb_s3_download.add_argument('--s3path', required=True, help='Path to S3')

    # Sub-parser for creating a database
    sb_create = subparsers.add_parser('create_db', description='Create database')
    sb_create.add_argument('--engine_string', default=SQLALCHEMY_DATABASE_URI,
                           help='SQLAlchemy connection URI for database')

    args = parser.parse_args()
    sp_used = args.subparser_name
    if sp_used == 's3_upload':
        upload_file_to_s3(args.local_path, args.s3path)
    elif sp_used == 's3_download':
        download_file_from_s3(args.local_path, args.s3path)
    elif sp_used == 'create_db':
        create_db(args.engine_string)
    else:
        parser.print_help()
