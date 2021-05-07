import argparse
import logging.config

from config.flaskconfig import SQLALCHEMY_DATABASE_URI
from src.create_mysql import create_db
from src.s3 import upload_file_to_s3

logging.config.fileConfig('config/logging/local.conf')
logger = logging.getLogger(__name__)

if __name__ == '__main__':

    # Create parser
    parser = argparse.ArgumentParser(description="Create database or upload data to S3")
    subparsers = parser.add_subparsers(dest="subparser_name")

    # Sub-parser for uploading data to S3 bucket
    sb_s3 = subparsers.add_parser("s3_upload", description="Upload data to S3")
    sb_s3.add_argument('--s3path', help="Where to load data to in S3")
    sb_s3.add_argument('--local_path', help="Where data exists in local")

    # Sub-parser for creating a database
    sb_create = subparsers.add_parser("create_db", description="Create database")
    sb_create.add_argument("--engine_string", default=SQLALCHEMY_DATABASE_URI,
                           help="SQLAlchemy connection URI for database")

    args = parser.parse_args()
    sp_used = args.subparser_name
    if sp_used == 's3_upload':
        upload_file_to_s3(args.local_path, args.s3path)
    elif sp_used == 'create_db':
        create_db(args.engine_string)
    else:
        parser.print_help()
