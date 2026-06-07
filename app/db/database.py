from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.db.settings import getSettings
settings = getSettings()
Base = declarative_base()
engine = create_engine(url=f"postgresql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_DB}")
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def getDatabase():
    session = Session()
    try:
        yield session
    finally:
        session.close()