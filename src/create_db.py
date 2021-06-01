import logging.config

import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

from sqlalchemy import create_engine

import warnings
from sqlalchemy import exc as sa_exc

logger = logging.getLogger(__name__)

Base = declarative_base()


class Hike(Base):
    """Create a data model for the database to be set up for capturing national park trails."""

    __tablename__ = 'trails'

    trail_id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=False, nullable=False)
    area_name = Column(String(50), unique=False, nullable=False)
    city_name = Column(String(50), unique=False, nullable=False)
    state_name = Column(String(20), unique=False, nullable=False)
    country_name = Column(String(20), unique=False, nullable=False)
    _geoloc = Column(String(50), unique=False, nullable=False)
    popularity = Column(Float, unique=False, nullable=False)
    length = Column(Float, unique=False, nullable=False)
    elevation_gain = Column(Float, unique=False, nullable=False)
    difficulty_rating = Column(Integer, unique=False, nullable=False)
    route_type = Column(String(20), unique=False, nullable=False)
    visitor_usage = Column(Integer, unique=False, nullable=False)
    avg_rating = Column(Float, unique=False, nullable=False)
    num_reviews = Column(Integer, unique=False, nullable=False)
    features = Column(String(100), unique=False, nullable=False)
    activities = Column(String(100), unique=False, nullable=False)
    units = Column(String(10), unique=False, nullable=False)

    def __repr__(self):
        return '<Hike: %r>' % self.name


def create_db(engine_string: str) -> None:
    """Create database from provided engine string.

    Args:
        engine_string (str): engine string for connecting to the sql database

    Returns:
        None
    """

    try:
        logger.debug('Connecting to SQLAlchemy.')
        engine = sqlalchemy.create_engine(engine_string)
        Base.metadata.create_all(engine)
        logger.info('Database successfully created.')
    except sqlalchemy.exc.OperationalError:
        logger.error('Database could not be created.')
        logger.warning('Make sure you are connected to Northwestern VPN.')
    # else:
    #     logger.info('Database could not be created.')


def insert_all(engine_string, data_path):
    """insert csv in sql"""
    engine = create_engine(engine_string, echo=False)

    # Read data as df
    with open(data_path, 'r', encoding='utf-8') as file:
        df = pd.read_csv(file, index_col=0)

    #  Warning: (1366, "Incorrect string value: '\\xC4\\x81ulu ...' for column 'name' at row 365")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        df.to_sql('trails', con=engine, if_exists='replace')


class HikeManager:

    def __init__(self, app=None, engine_string=None):
        """Manage Flask to SQLAlchemy connection.

        Args:
            app: Flask - Flask app
            engine_string: str - Engine string
        """
        if app:
            # Create flask app
            self.db = SQLAlchemy(app)
            self.session = self.db.session
        elif engine_string:
            # Create SQL alchemy engine and session
            engine = sqlalchemy.create_engine(engine_string)
            Session = sessionmaker(bind=engine)
            self.session = Session()
        else:
            raise ValueError('Need either an engine string or a Flask app to initialize')
            logger.error('Engine string or Flask app has not been provided.')

    def close(self) -> None:
        """Closes session

        Returns:
            None
        """
        self.session.close()

    def add_trail(self,
                  trail_id: int,
                  name: str,
                  area_name: str,
                  city_name: str,
                  state_name: str,
                  country_name: str,
                  _geoloc: str,
                  popularity: float,
                  length: float,
                  elevation_gain: float,
                  difficulty_rating: int,
                  route_type: str,
                  visitor_usage: int,
                  avg_rating: float,
                  num_reviews: int,
                  features: str,
                  activities: str,
                  units: str) -> None:
        """Seeds an existing database with additional songs.
        Args:
            title: str - Title of song
            artist: str - Artist
            album: str - Album title
        Returns:None
        """

        session = self.session
        trail = Hike(trail_id=trail_id,
                     name=name,
                     area_name=area_name,
                     city_name=city_name,
                     state_name=state_name,
                     country_name=country_name,
                     _geoloc=_geoloc,
                     popularity=popularity,
                     length=length,
                     elevation_gain=elevation_gain,
                     difficulty_rating=difficulty_rating,
                     route_type=route_type,
                     visitor_usage=visitor_usage,
                     avg_rating=avg_rating,
                     num_reviews=num_reviews,
                     features=features,
                     activities=activities,
                     units=units)
        session.add(trail)
        session.commit()
        # logger.info("%s by %s from album, %s, added to database", title, artist, album)
