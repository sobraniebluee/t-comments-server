import sqlalchemy as db
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.engine import create_engine
from src.config import Config
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(Config.DB_CONN, echo=False)
session_factory = sessionmaker(bind=engine, autoflush=False)
session = scoped_session(session_factory)
Base = declarative_base()
Base.query = session.query_property()


def create_metadata():
    Base.metadata.create_all(bind=engine)
