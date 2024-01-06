from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from atom.core import config

SQLALCHEMY_DATABASE_URL = config.settings.DATABASE_URL

# to create a database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# session configures the session to be used for database operations.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# declarative_base serves as the base class for declarative models that will be created

Base = declarative_base()


# It creates a database session (db) using SessionLocal and yields it to the caller.
# After the execution within the context is completed, the finally block ensures that the session is closed.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
