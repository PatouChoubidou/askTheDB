from sqlalchemy import ForeignKey
from sqlalchemy import String, text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import select, insert, update
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


class Base(DeclarativeBase):   
    pass

class Bookmarks(Base):
    __tablename__ = "Bookmarks"

    bookmark_ID: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str]
    sql: Mapped[str]
    user_ID: Mapped[int] = mapped_column(ForeignKey("user.user_ID"))
    created_at: Mapped[str]
    
    def __repr__(self) -> str:
        return f"Bookmarks(bookmark_ID={self.bookmark_ID!r}, question={self.question!r}, sql={self.sql!r}, user_ID={self.user_ID!r}, created_at={self.created_at!r} )"
    
# works
async def getBookmarks():
    print('inside get all bookmarks')

    engine = create_engine(os.environ.get('APP_DB_URL'))
    conn = engine.connect()
    stmt = select(Bookmarks)
    result =  conn.execute(stmt)
    conn.close()
    allBookmarks = []
    print(result)
    for item in result:
        allBookmarks.append({
        "bookmark_ID": item.bookmark_ID,
        "question": item.question,
        "sql": item.sql,
        "user_ID": item.user_ID, 
        "created_at": item.created_at
    })
    print(allBookmarks)   
    return allBookmarks

# work
async def createBookmark(q: String, sql: String, user_ID: int):
    print('inside create bookmark')
    try:
        engine = create_engine(os.environ.get('APP_DB_URL'))
        conn = engine.connect()
        isIn = await checkWheaterBookmarkQuestionExits(q)
        if(isIn):
            stmt = update(Bookmarks).where(Bookmarks.question == q).values(question=q, sql=sql, user_ID=user_ID)
        else:
            stmt = insert(Bookmarks).values(question=q, sql=sql, user_ID=user_ID)
        print(stmt)
        result = conn.execute(stmt)
        conn.commit()
        conn.close()
        return result
    except:
        print('failure in create bookmark')


async def checkWheaterBookmarkQuestionExits(question: str):
    isIn = False 
    allBookmarks = await getBookmarks()
    for bookmark in allBookmarks:
        q = bookmark['question']
        if(q == question):
            isIn = True
            return isIn
    print('check wheter bookmark with question exits = ', isIn)
    return isIn
    
# works
async def getBookmarkByID(id):
    print('inside get create bookmarks')
    try:
        engine = create_engine(os.environ.get('APP_DB_URL'))
        conn = engine.connect()
        stmt = text("SELECT * FROM Bookmarks WHERE bookmark_ID = " + str(id) + ";")
        result = conn.execute(stmt)
        allBookmarks = []
        print(result)
        for item in result:
            allBookmarks.append({
            "bookmark_ID": item.bookmark_ID,
            "question": item.question,
            "sql": item.sql,
            "user_ID": item.user_ID, 
            "created_at": item.created_at
        })
        print(allBookmarks)   
        return allBookmarks[0]
    except:
        print('failure in bookmark by id')


async def getBookmarksByUserID(id):
    print('inside get create bookmarks, id is: ', id, type(id))
    try:
        engine = create_engine(os.environ.get('APP_DB_URL'))
        conn = engine.connect()
        stmt = text("SELECT * FROM Bookmarks boo WHERE boo.user_ID = " + str(id) + ";")
        result = conn.execute(stmt)
        allBookmarks = []
        for item in result:
            allBookmarks.append({
            "bookmark_ID": item.bookmark_ID,
            "question": item.question,
            "sql": item.sql,
            "user_ID": item.user_ID, 
            "created_at": item.created_at
        })  
        return allBookmarks
    except:
        print('failure in bookmark by id')


async def getBookmarkInCategorie(cat: str):
    print('inside get bookmarks in categorie')
    print(cat)
    try:
        engine = create_engine(os.environ.get('APP_DB_URL'))
        conn = engine.connect()
        stmt = text("""SELECT * FROM Bookmarks boo 
                    INNER JOIN BookmarkCategories bocat 
                    ON boo.bookmark_ID = bocat.bookmark_ID 
                    INNER JOIN Categories cat 
                    ON cat.categorie_ID = bocat.categorie_ID 
                    WHERE cat.categorie = '""" + cat + "';")
        result = conn.execute(stmt)
        
        allBookmarks = []
        print(result)
        for item in result:
            allBookmarks.append({
            "bookmark_ID": item.bookmark_ID,
            "question": item.question,
            "sql": item.sql,
            "user_ID": item.user_ID, 
            "created_at": item.created_at
        })  
        return allBookmarks
    except:
        print('failure in get bookmark in categorie')


# works
async def deleteBookmarkByID(id):
    print('inside get delete bookmarks')
    try:
        engine = create_engine(os.environ.get('APP_DB_URL'))
        conn = engine.connect()
        stmt = text("DELETE FROM Bookmarks WHERE bookmark_ID = " + str(id) + ";")
        result = conn.execute(stmt)
        conn.commit()
        conn.close()
        return result
    except:
        print('failure in delete bookmark by id')
      
