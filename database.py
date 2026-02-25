from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
engine = create_engine(
    "sqlite:///mydata.db",
    echo = True
)
Base = declarative_base()


Session = sessionmaker(bind=engine)
session = Session()