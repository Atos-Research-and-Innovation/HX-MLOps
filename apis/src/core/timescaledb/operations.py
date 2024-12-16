import os
import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
from src.core.logger_session import logger


def create_tables(Base):
    url = get_url_from_env()
    engine = get_engine(url)
    Base.metadata.create_all(bind=engine)
    logger.info(f"The whole tables created at: {url}")


def create_db():
    url = get_url_from_env()
    engine = get_engine(url)
    if not database_exists(engine.url):
        create_database(engine.url)
        logger.info(f"Database created: {url}")


def reset_database(Base):
    url = get_url_from_env()
    engine = get_engine(url)
    if database_exists(engine.url):
        drop_database(engine.url)
        logger.info(f"Database deleted:  {url}")
    
    create_database(engine.url)
    logger.info(f"Database created:  {url}")

    Base.metadata.create_all(bind=engine)
    logger.info(f"The whole tables created at: {url}")


def get_session():
    url = get_url_from_env()
    engine = get_engine(url)
    session = sessionmaker(bind=engine)()
    return session


def check_connection():
    try:
        session = get_session()
        result = session.execute(text("SELECT 1"))
        session.close()
        return True
    except:
        return False

# -------------------------------------------------------

def get_engine(url):
    engine = create_engine(url, pool_size=50, echo=False)
    return engine


def get_url_from_env():

    user = os.environ.get("POSTGRES_USER")
    passwd = os.environ.get("POSTGRES_PASSWORD")
    host = os.environ.get("POSTGRES_HOST")
    port = os.environ.get("POSTGRES_PORT")
    dbname = os.environ.get("POSTGRES_DBNAME")

    url = f"postgresql://{user}:{passwd}@{host}:{port}/{dbname}"

    return url
