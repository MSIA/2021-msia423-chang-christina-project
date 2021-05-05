import logging.config

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, MetaData
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger(__name__)
logger.setLevel("INFO")

Base = declarative_base()


class Trails(Base):
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
        return '<Trail: %r>' % self.name


def create_db(engine_string: str) -> None:
    """Create database from provided engine string

    Args:
        engine_string: str - Engine string

    Returns: None

    """
    try:
        engine = sqlalchemy.create_engine(engine_string)
        Base.metadata.create_all(engine)
        logger.info("Database created.")
    except:
        logger.info("Database cannot be created.")
