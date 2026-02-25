from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from sqlalchemy import create_engine

engine = create_engine(
    "sqlite:///mydata.db",
    echo=True
)

Base = declarative_base()

Session = scoped_session(sessionmaker(bind=engine))