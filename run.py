import argparse

import logging.config
logging.config.fileConfig('config/logging/local.conf')
#logger = logging.getLogger('penny-lane-pipeline')

#from src.add_songs import TrackManager, create_db
from src.s3 import upload_file_to_s3
from src.create_tables import create_db
from config.flaskconfig import SQLALCHEMY_DATABASE_URI

if __name__ == '__main__':

    # Add parsers for both creating a database
    parser = argparse.ArgumentParser(description="Create database")
    subparsers = parser.add_subparsers()

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
    if sp_used == 'create_db':
        create_db(args.engine_string)
    elif sp_used == 's3_upload':
        upload_file_to_s3(args.local_path, args.s3path)
    # elif sp_used == 'ingest':
    #     tm = TrackManager(engine_string=args.engine_string)
    #     tm.add_track(args.title, args.artist, args.album)
    #     tm.close()
    else:
        parser.print_help()



