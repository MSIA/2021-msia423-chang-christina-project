import logging.config
import warnings

import pandas as pd
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

Base = declarative_base()


class Input(Base):
    """Create a data model for the database to be set up for capturing national
    park trails."""

    __tablename__ = 'input'
    input_id = Column(String(100), primary_key=True)
    length = Column(Float, unique=False, nullable=False)
    elevation_gain = Column(Float, unique=False, nullable=False)
    route_type = Column(String(100), unique=False, nullable=False)
    features = Column(String(100), unique=False, nullable=False)
    activities = Column(String(100), unique=False, nullable=False)

    def __repr__(self):
        return '<Input: %r>' % self.name


class Trails(Base):
    """Create a data model for the database to be set up for capturing national
    park trails."""

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
        return '<Trails: %r>' % self.name


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


def insert_all(engine_string, data_path, table_name):
    """Insert csv into sql table."""
    engine = create_engine(engine_string, echo=False)

    # Read data as df
    with open(data_path, 'r', encoding='utf-8') as file:
        df = pd.read_csv(file, index_col=0)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        df.to_sql(table_name, con=engine, if_exists='replace')


class TrailManager:

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
            raise ValueError('Need either an engine string or a Flask app to '
                             'initialize')
            logger.error('Engine string or Flask app has not been provided.')

    def close(self) -> None:
        """Closes session

        Returns:
            None
        """
        self.session.close()

    def add_input(self,
                  input_id: str,
                  length: float,
                  elevation_gain: float,
                  route_type: str,
                  features: str,
                  activities: str) -> None:

        """Seeds an existing database with user input trails.

        Args:
            input_id (str): unique id of trail
            length (float): length of trail
            elevation_gain (float): elevation gain of trail
            route_type (str): route type of trail
            features (str): features of trail
            activities (str): activities of trail

        Returns:
            None

        """

        session = self.session
        input = Input(input_id=input_id,
                      length=length,
                      elevation_gain=elevation_gain,
                      route_type=route_type,
                      features=features,
                      activities=activities)
        session.add(input)
        session.commit()
