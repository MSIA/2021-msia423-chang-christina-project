import logging.config

import pandas as pd
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, MetaData
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger(__name__)
logger.setLevel("INFO")

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
    """Create database from provided engine string
    Args:
        engine_string: str - Engine string
    Returns: None
    """
    engine = sqlalchemy.create_engine(engine_string)
    Base.metadata.create_all(engine)
    logger.info("Database created.")


class HikeManager:

    def __init__(self, app=None, engine_string=None):
        """
        Args:
            app: Flask - Flask app
            engine_string: str - Engine string
        """
        if app:
            self.db = SQLAlchemy(app)
            self.session = self.db.session
        elif engine_string:
            engine = sqlalchemy.create_engine(engine_string)
            Session = sessionmaker(bind=engine)
            self.session = Session()
        else:
            raise ValueError("Need either an engine string or a Flask app to initialize")

    def close(self) -> None:
        """Closes session
        Returns: None
        """
        self.session.close()

    def add_dataset(self, path, table_name="trails"):
        """
        Inserts data from CSV file into existing database.

        Args:
            path (str): path to CSV file
            table_name (str): name of database in SQL database

        Returns: None
        """
        session = self.session
        df = pd.read_csv(path)
        df.to_sql(name=table_name, con=session, index=False, if_exists="replace")
        session.commit()
        logger.info("Contents of %s added to database", path)
