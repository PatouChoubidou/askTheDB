from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, DateTime, text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Session
from sqlalchemy import select, insert
from sqlalchemy import create_engine
from sqlalchemy.sql import func
import datetime
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


class Base(DeclarativeBase):   
    pass


class Ratings(Base):
    __tablename__ = "Ratings"

    rating_ID: Mapped[int] = mapped_column(primary_key=True)
    question_ID: Mapped[int] = mapped_column(ForeignKey("questions.question_ID"))
    q_interpretation: Mapped[float]
    sql_quality: Mapped[float]
    created_at: Mapped[str]
    
    def __repr__(self) -> str:
        return f"Ratings(rating_ID={self.rating_ID!r}, question_ID={self.question_ID!r}, q_interpretation={self.q_interpretation!r}, sql_quality={self.sql_quality!r}, created_at={self.created_at!r} )"
    

async def getRatings():
    print('inside get all ratings')

    engine = create_engine(os.environ.get('APP_DB_URL'))
    conn = engine.connect()
    stmt = select(Ratings)
    result =  conn.execute(stmt)
    conn.close()
    allRatings = []
    print(result)
    for item in result:
        allRatings.append({
        "rating_ID": item.rating_ID,
        "question_ID": item.question_ID,
        "q_interpretation": item.q_interpretation,
        "sql_quality": item.sql_quality, 
        "created_at": item.created_at
    })
    print(allRatings)   
    return allRatings


async def createRating(q_ID: int, q_interpretation: float, sql_quality: float):
    print('inside get create rating')
    try:
        engine = create_engine(os.environ.get('APP_DB_URL'))
        conn = engine.connect()
        stmt = insert(Ratings).values(question_ID=q_ID, q_interpretation=q_interpretation, sql_quality=sql_quality)
        result = conn.execute(stmt)
        conn.commit()
        conn.close()
        return result
    except:
        print('failure in create question')


async def getRatingByID(id: int):
    engine = create_engine('sqlite:///appDB/app.db')
    conn = engine.connect()
    stmt = text("SELECT * FROM RATINGS r WHERE r.rating_ID = "+ str(id) + ";")
    result =  conn.execute(stmt)
    conn.close()
    allRatings = []
    print(result)
    for item in result:
        allRatings.append({
        "rating_ID": item.rating_ID,
        "question_ID": item.question_ID,
        "q_interpretation": item.q_interpretation,
        "sql_quality": item.sql_quality, 
        "created_at": item.created_at
    })
    print(allRatings)   
    return allRatings[0]

'''
async def getBestRatedQuesitons():
    engine = create_engine(os.environ.get('APP_DB_URL'))
    conn = engine.connect()
    output = conn.execute(text('SELECT * FROM Question q INNER JOIN Ratings r ON q.question_ID = r.question_ID WHERE r.rating_interpretation >= 0.8 AND r.rating_sql >= 0.8'))
    result = output.fetchall()
    # hard-coded works :-(
    items = []
    for row in result:
        items.append({
        "question_ID": row[0],
        "question": row[1],
        "sql": row[2],
        "db_response": row[3], 
        "explanation": row[4],
        "user_ID": row[5],
        "created_at": row[6]
        })

    out = {"items": items}  
    conn.close()
    return out
    
'''