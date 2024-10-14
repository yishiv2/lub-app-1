import os

from sqlalchemy import Column, DateTime, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class WordSet(Base):
    __tablename__ = "word_sets"

    id = Column(Integer, primary_key=True, index=True)
    word1 = Column(String, nullable=False)
    word2 = Column(String, nullable=False)
    commonality = Column(Text)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


def init_db():
    Base.metadata.create_all(bind=engine)
