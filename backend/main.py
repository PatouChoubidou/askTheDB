import json
import re
from fastapi import FastAPI, Depends, HTTPException, status, Request  
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel
from typing import Annotated, Union
from passlib.context import CryptContext
from backend.llm import llm
from backend.appDB.models.users import dbGetUserByUsername
from backend.appDB.models.questions import getQuestions
from backend.appDB.models.questions import createQuestion
from backend.appDB.models.questions import getLatestQuestion
from backend.appDB.models.questions import countQuestions
from backend.appDB.models.questions import emptyQuestionsTable
from backend.appDB.models.questions import getQuestionAndRatings
from backend.appDB.models.ratings import getRatings
from backend.appDB.models.ratings import getRatingByID
from backend.appDB.models.ratings import createRating
from backend.appDB.models.bookmarks import getBookmarks
from backend.appDB.models.bookmarks import getBookmarkByID
from backend.appDB.models.bookmarks import deleteBookmarkByID
from backend.appDB.models.bookmarks import createBookmark
from backend.appDB.models.bookmarks import getBookmarksByUserID
from backend.appDB.models.bookmarks import getBookmarkInCategorie

from backend.appDB.models.databaseConnections import getDbConnectionsByUserID


from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
print(os.environ.get('APP_DB_URL'))


app = FastAPI()

# allow the frontend
origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# using Requests
@app.post("/askLLM/")
async def getQuestion(request: Request):
    payload = await request.json()
    response = await llm.askTheLLM(payload["question"])
    return response


@app.post("/sendSQL/")
async def resendQuery(request: Request):
    payload = await request.json()
    response = await llm.runSQLandExplain(payload["sql"], payload["question"])
    print(response)
    return response


@app.get("/getTables/")
async def getTables(request: Request):
    response = await llm.getDBTables()
    print(response)
    return response
 
# get a an array of strings with table create statements of db
@app.get("/getCreateStmts/")
async def getSQLiteCreateStmts(request: Request):
    response = await llm.getSQLiteCreateStmts()
    print(response)
    return response


# DB connections
# get all by user id
@app.get("/users/{user_id}/connections/")
async def getDbConnByUserId(user_id):
    response = await getDbConnectionsByUserID(user_id)
    print(response)
    return response


# QUESTIONS
#get all
@app.get("/questions/")
async def getAllQuestions():
    response = await getQuestions()
    return response


#create one
@app.post("/questions/")
async def createAQuestion(request: Request):
    payload = await request.json()
    question = payload["question"]
    sql = payload["sql"]
    db_response = payload["db_response"]
    explanation = payload["explanation"]
    user_ID = payload["user_ID"]
    response = await createQuestion(question, sql, db_response, explanation, user_ID)
       
    return response


# get last question created
@app.get("/questions/getLatest/")
async def getLastQuestion():
    response = await getLatestQuestion()
    return response


# count all questions
@app.get("/questions/count")
async def countTheQuestions():
    response = await countQuestions()
    return response


# get all questions and their rating
@app.get("/questions/ratings")
async def getQuestionsWithRatings():
    response = await getQuestionAndRatings()
    return response


# delete all will delete associated ratings as well
# the on delete cascade is not working yet :-(
'''
@app.post("/questions/deleteAll")
async def emptyAllQuestions():
    response = await emptyQuestionsTable()
    return response
'''

# RATINGS
# get all
@app.get("/ratings/")
async def getAllRatings():
    response = await getRatings()
    print(response)
    return response


# get by id
@app.get("/ratings/{id}")
async def getRatingById(id: int):
    response = await getRatingByID(id)
    print(response)
    return response


# create  
@app.post("/ratings/")
async def createtRating(request: Request):
    payload = await request.json()

    q = payload["question"]
    sql = payload["sql"]
    db_response = payload["db_response"]
    explanation = payload["explanation"]
    user_ID = payload['user_ID']
    # first create a new question
    await createQuestion(q, sql, db_response, explanation, user_ID)
    # then get the id
    lastQ = await getLatestQuestion()
    lastQ_id = lastQ['question_ID']
    question_ID = lastQ_id
    q_interpretation = payload["q_interpretation"]
    sql_quality = payload["sql_quality"]
    response = await createRating(question_ID, q_interpretation, sql_quality)
    return response


# BOOKMARKS
# get all
@app.get("/bookmarks/")
async def getAllBookmarks():
    response = await getBookmarks()
    print(response)
    return response


# get single
@app.get("/bookmarks/{id}")
async def getBookmarkById(id: int):
    response = await getBookmarkByID(id)
    print(response)
    return response


# get all by user id
@app.get("/users/{user_id}/bookmarks/")
async def getBookmarkByUserId(user_id):
    response = await getBookmarksByUserID(user_id)
    print(response)
    return response


# get all bookmarks by categorie
@app.get("/bookmarks/categorie/")
async def getBookmarkByCategorie(cat: str):
    print(cat)
    response = await getBookmarkInCategorie(cat)
    print(response)
    return response


# create bookmark
@app.post("/bookmarks/")
async def createABookmark(request: Request):
    payload = await request.json()
    question = payload["question"]
    sql = payload["sql"]
    user_ID = payload["user_ID"]
    response = await createBookmark(question, sql, user_ID)
    print(response)
    return response


# delete single
@app.delete("/bookmarks/{id}")
async def deleteABookmarkById(id: int):
    response = await deleteBookmarkByID(id)
    print(response)
    return response





