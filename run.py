# import argparse
# import logging.config

import argparse
import logging

import pandas as pd
import yaml

from config.flaskconfig import SQLALCHEMY_DATABASE_URI
from src.s3 import upload_file_to_s3, download_file_from_s3
from src.create_db import create_db
import src.clean as clean
import src.featurize as featurize
import src.model as model

logging.config.fileConfig('config/logging/local.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

# Create parser
parser = argparse.ArgumentParser(description='Create database or upload data to S3')
parser.add_argument('--config', default='config/project.yaml', help='Path to configuration file')
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
sb_create.add_argument('--data_path',  help='Insert data into database')

# Sub-parser for cleaning data
sb_clean = subparsers.add_parser('clean', description='Clean data')

# Sub-parser for creating features
sb_featurize = subparsers.add_parser('featurize', description='Create features')

# Sub-parser for creating features
sb_model = subparsers.add_parser('model', description='Run model')

# Get parser
args = parser.parse_args()
sp_used = args.subparser_name


if __name__ == '__main__':

    # Load configuration file for parameters and tmo path
    with open(args.config, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    logger.info("Configuration file loaded from %s" % args.config)

    if sp_used == 's3_upload':
        upload_file_to_s3(args.local_path, args.s3path)
    elif sp_used == 's3_download':
        download_file_from_s3(args.local_path, args.s3path)
    elif sp_used == 'create_db':
        create_db(args.engine_string)
    elif sp_used == 'clean':
        clean.clean(**config['clean']['clean'])
    elif sp_used == 'featurize':
        featurize.featurize(**config['featurize']['featurize'])
    elif sp_used == 'model':
        model.model(**config['model']['model'])
    else:
        parser.print_help()
