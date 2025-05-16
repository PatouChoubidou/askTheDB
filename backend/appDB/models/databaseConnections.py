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
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Base(DeclarativeBase):   
    pass


class DatabaseConnections(Base):
    __tablename__ = "DatabaseConnections"

    connection_ID: Mapped[int] = mapped_column(primary_key=True)
    conn_string: Mapped[str]
    user_ID: Mapped[int] = mapped_column(ForeignKey("users.user_ID"))
    type: Mapped[Optional[str]]
    driver: Mapped[Optional[str]]
    dialect: Mapped[Optional[str]]
    username: Mapped[Optional[str]]
    hashed_password: Mapped[Optional[str]]
    host: Mapped[Optional[str]]
    port: Mapped[Optional[int]]
    database_name: Mapped[Optional[str]]
    created_at: Mapped[str]
    
    def __repr__(self) -> str:
        return f'''DatabaseConnection(
        connection_ID={self.connection_ID!r}, 
        conn_string={self.conn_string!r}, 
        user_ID={self.user_ID!r}, 
        type={self.type!r}, 
        driver={self.driver!r}, 
        dialect={self.dialect!r}, 
        username={self.username!r}, 
        hashed_password={self.hashed_password!r},
        host={self.host!r},
        port={self.port!r},
        database_name={self.database_name!r},
        created_at={self.created_at!r} )'''


async def getDbConnections():
    print('inside get all db questions')

    engine = create_engine(os.environ.get('APP_DB_URL'))
    conn = engine.connect()
    stmt = select(DatabaseConnections)
    result = conn.execute(stmt)
    conn.close()
    allConns = []
    print(result)
    for item in result:
        allConns.append({
        "connection_ID": item.connection_ID,
        "conn_string": item.conn_string,
        "user_ID": item.user_ID,
        "type": item.type, 
        "driver": item.driver, 
        "dialect": item.dialect,
        "username": item.username,
        "hashed_password": item.hashed_password,
        "host": item.host,
        "port": item.port,
        "database_name": item.databse_name,
        "created_at": item.created_at
    })
    print(allConns)   
    return allConns


async def getDbConnectionsByUserID(id):
    print('inside get create db connection, id is: ', id, type(id))
    try:
        engine = create_engine(os.environ.get('APP_DB_URL'))
        conn = engine.connect()
        stmt = text("SELECT * FROM DatabaseConnections con WHERE con.user_ID = " + str(id) + ";")
        print(stmt)
        result = conn.execute(stmt)

        allConns = []
        for item in result:
            allConns.append({
            "connection_ID": item.connection_ID,
            "conn_string": item.conn_string,
            "user_ID": item.user_ID,
            "type": item.type, 
            "driver": item.driver, 
            "dialect": item.dialect,
            "username": item.username,
            "hashed_password": item.hashed_password,
            "host": item.host,
            "port": item.port,
            "database_name": item.database_name,
            "created_at": item.created_at
        })  
        return allConns
    except:
        print('failure in dbConnections by id')


async def createDbConnection(conn_string: str, user_ID: int, type: str, driver: str, dialect: str, username: str, hashed_password: str, host: str, port: int, databse_name: str):
    print('inside get create db connection')
    try:
        engine = create_engine(os.environ.get('APP_DB_URL'))
        conn = engine.connect()
        stmt = insert(DatabaseConnections).values(conn_string=conn_string, user_ID=user_ID, type=type, driver=driver, dialect=dialect, username=username, hashed_password=hashed_password, host=host, port=port, databse_name=databse_name)
        result = conn.execute(stmt)
        conn.commit()
        conn.close()
        return result
    except:
        print('failure in create dbConnection')