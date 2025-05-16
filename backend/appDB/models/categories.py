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

class Categorie(Base):
    __tablename__ = "Categories"

    categorie_ID: Mapped[int] = mapped_column(primary_key=True)
    categorie: Mapped[str]
    
    def __repr__(self) -> str:
        return f"Categorie(categorie_ID={self.categorie_ID!r}, categorie={self.categorie!r})"
    

class BookmarksCategorie(Base):
    __tablename__ = "BookmarkCategories"

    bookmark_categorie_ID: Mapped[int] = mapped_column(primary_key=True)
    categorie_ID: Mapped[int] = mapped_column(ForeignKey("categorie.categorie_ID"))
    bookmark_ID: Mapped[int] = mapped_column(ForeignKey("bookmark.bookmark_ID"))

    def __repr__(self) -> str:
        return f"BookmarksCategorie(bookmark_categorie_ID={self.bookmark_categorie_ID!r}, categorie_ID={self.categorie_ID!r}, bookmark_ID={self.bookmark_ID!r})"
    

async def getCategeries():
    print('inside get all bookmarks')

    engine = create_engine(os.environ.get('APP_DB_URL'))
    conn = engine.connect()
    stmt = select(Categorie)
    result =  conn.execute(stmt)
    conn.close()
    allRows = []
    print(result)
    for row in result:
        allRows.append({
        "categorie_ID": row.categorie_ID,
        "categorie": row.categorie
    })
    print(allRows)   
    return allRows


async def createCategorie(cat: String):
    print('inside get create categorie')
    try:
        engine = create_engine(os.environ.get('APP_DB_URL'))
        conn = engine.connect()
        stmt = insert(Categorie).values(categorie=cat)
        print(stmt)
        result = conn.execute(stmt)
        conn.commit()
        conn.close()
        return result
    except:
        print('failure in create bookmark')


async def getCategerieIdByName(cat_name: String):
    print('inside get categorie by name')

    engine = create_engine(os.environ.get('APP_DB_URL'))
    conn = engine.connect()
    stmt = text("SELECT * FROM Categories cat WHERE cat.categorie = '"+ cat_name + "';")
    result =  conn.execute(stmt)
    conn.close()
    allRows = []
    print(result)
    for row in result:
        allRows.append({
        "categorie_ID": row.categorie_ID,
        "categorie": row.categorie
    })
    print(allRows)   
    return allRows[0]


async def deleteCategorieByName(cat: String):
    print('inside get create categorie')
    try:
        engine = create_engine(os.environ.get('APP_DB_URL'))
        conn = engine.connect()
        stmt = text("DELETE FROM Categories cat WHERE cat.categorie = '" + cat + "';")
        result = conn.execute(stmt)
        conn.commit()
        conn.close()
        print(result)
        return result
    except:
        print('failure in create bookmark')


    
