from datetime import datetime
from typing import List, Optional

from fastapi import Depends, FastAPI, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from db import SessionLocal, WordSet

app = FastAPI()


# Pydantic models for responses
class WordSetResponse(BaseModel):
    id: int
    word1: str
    word2: str
    commonality: str
    created_at: datetime

    class Config:
        orm_mode = True  # Allows conversion from SQLAlchemy models to Pydantic models


class AvailableDatesResponse(BaseModel):
    available_dates: List[str]


# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# API endpoint for fetching word sets
@app.get("/word_sets/", response_model=List[WordSetResponse])
def get_word_sets(
    date: Optional[str] = Query(
        None, description="フォーマットはYYYY-MM-DD", example="2024-10-14"
    ),
    db: Session = Depends(get_db),
):
    if date:
        try:
            target_date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            return {"error": "Invalid date format. Use YYYY-MM-DD."}

        word_sets = (
            db.query(WordSet).filter(func.date(WordSet.created_at) == target_date).all()
        )
    else:
        word_sets = db.query(WordSet).all()

    return word_sets


# API endpoint for fetching available dates
@app.get("/word_sets/dates/", response_model=AvailableDatesResponse)
def get_available_dates(db: Session = Depends(get_db)):
    dates = db.query(func.date(WordSet.created_at)).distinct().all()
    available_dates = [date[0].strftime("%Y-%m-%d") for date in dates]

    return {"available_dates": available_dates}
