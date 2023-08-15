from sqlalchemy.ext.declarative import declarative_base, as_declarative
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///./gift_app.db?check_same_thread=False"


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Session = scoped_session(SessionLocal)


Base = declarative_base()

