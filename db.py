from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

engine = create_engine("sqlite:///database.db",echo=True)

Base = declarative_base()

Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)