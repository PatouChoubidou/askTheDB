from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import select, insert
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

class Base(DeclarativeBase):   
    pass

class Questions(Base):
    __tablename__ = "Questions"

    question_ID: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str]
    sql: Mapped[str]
    db_response: Mapped[Optional[str]]
    explanation: Mapped[Optional[str]]
    user_ID: Mapped[int] = mapped_column(ForeignKey("user.user_ID"))
    created_at: Mapped[str]
    
    def __repr__(self) -> str:
        return f"Questions(question_ID={self.question_ID!r}, question={self.question!r}, sql={self.sql!r}, db_response={self.db_response!r}, explanation={self.explanation!r}, user_ID={self.user_ID!r}, created_at={self.created_at!r} )"
    

# works
async def getQuestions():
    print('inside get all questions')

    engine = create_engine(os.environ.get('APP_DB_URL'))
    conn = engine.connect()
    stmt = select(Questions)
    result =  conn.execute(stmt)
    conn.close()
    allQuestions = []
    print(result)
    for item in result:
        allQuestions.append({
        "question_ID": item.question_ID,
        "question": item.question,
        "sql": item.sql,
        "db_response": item.db_response, 
        "explanation": item.explanation,
        "user_ID": item.user_ID,
        "created_at": item.created_at
    })

    print(allQuestions)  
    return allQuestions


# works
async def getLatestQuestion():
    print('inside get all questions')

    engine = create_engine(os.environ.get('APP_DB_URL'))
    conn = engine.connect()
    stmt = text("""SELECT * FROM Questions q WHERE q.question_ID IN (SELECT MAX(question_ID) FROM Questions);""")
    result = conn.execute(stmt)
    conn.close()
    lastQuestion = []
    print(result)
    for item in result:
        lastQuestion.append({
        "question_ID": item.question_ID,
        "question": item.question,
        "sql": item.sql,
        "db_response": item.db_response, 
        "explanation": item.explanation,
        "user_ID": item.user_ID,
        "created_at": item.created_at
    })
    print(lastQuestion)  
    return lastQuestion[0]
    

# works
async def createQuestion(q: String, sql: String, db_response: String, explanation: String, user_ID: int):
    questions_maximum = 1000
    if(await countQuestions() <= questions_maximum):
        try:
            engine = create_engine(os.environ.get('APP_DB_URL'))
            conn = engine.connect()
            print(conn)
            stmt = insert(Questions).values(question=q, sql=sql, db_response=db_response, explanation=explanation, user_ID=user_ID)
            print(stmt)
            result = conn.execute(stmt)
            conn.commit()
            conn.close()
            return result
        except:
            print('failure in create question')
    else:
        await emptyQuestionsTable()
        try:
            engine = create_engine(os.environ.get('APP_DB_URL'))
            conn = engine.connect()
            print(conn)
            stmt = insert(Questions).values(question=q, sql=sql, db_response=db_response, explanation=explanation, user_ID=user_ID)
            print(stmt)
            result = conn.execute(stmt)
            conn.commit()
            conn.close()
            return result
        except:
            print('failure in create question')
    print('inside get create question')
    


async def countQuestions():
    try:
        engine = create_engine(os.environ.get('APP_DB_URL'))
        conn = engine.connect()
        print(conn)
        stmt = text('SELECT COUNT(*) FROM Questions;')
        print(stmt)
        result = conn.execute(stmt)
        conn.commit()
        conn.close()
        return result.first()[0]
    except:
        print('failure in create question')


async def getQuestionAndRatings():
    print('inside get questions and Ratings')

    engine = create_engine(os.environ.get('APP_DB_URL'))
    conn = engine.connect()
    stmt = text("""SELECT * FROM Questions q 
                JOIN Ratings r
                ON q.question_ID = r.question_ID;""")
    result = conn.execute(stmt)
    conn.close()
    allQuestionRatings = []
    print(result)
    for item in result:
        allQuestionRatings.append({
        "question_ID": item.question_ID,
        "question": item.question,
        "sql": item.sql,
        "db_response": item.db_response, 
        "explanation": item.explanation,
        "user_ID": item.user_ID,
        "created_at": item.created_at,
        "rating_ID": item.rating_ID,
        "q_interpretation": item.q_interpretation,
        "sql_quality": item.sql_quality,
    })
    print(allQuestionRatings)  
    return allQuestionRatings


# not tested yet       
async def emptyQuestionsTable():
    # constraint to delete all ratings as well is not working yet?
    print('inside get empty question table')
    try:
        engine = create_engine(os.environ.get('APP_DB_URL'))
        conn = engine.connect()
        print(conn)
        stmt = text('DELETE FROM Questions; ')
        print(stmt)
        result = conn.execute(stmt)
        conn.commit()
        stmt2 = text('VACUUM')
        print(stmt2)
        result = conn.execute(stmt2)
        conn.close()
        return result
    except:
        print('failure in create question')
        return



