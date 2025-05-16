from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, DateTime, text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import create_engine
from sqlalchemy.sql import func
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Base(DeclarativeBase):   
    pass

class User(Base):
    __tablename__ = "Users"

    user_ID: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str]
    first_name: Mapped [Optional[int]]
    last_name: Mapped [Optional[int]]
    disabled: Mapped [Optional[int]]
    hashed_password: Mapped[str]
    created_at: Mapped[str]
    
    def __repr__(self) -> str:
        return f"User(user_ID={self.user_ID!r}, username={self.username!r}, email={self.email!r}, first_name={self.first_name!r}, last_name={self.last_name!r}, pw={self.hashed_password!r}), disabled={self.created_at!r}"

'''
class UserInDB(Base):
    __tablename__ = "UsersInDB"

    userInDB_ID: Mapped[int] = mapped_column(primary_key=True)
    user_ID: Mapped[int] = mapped_column(ForeignKey("user.user_ID"))
    hashed_password: Mapped[str]
    
    def __repr__(self) -> str:
        return f"UserInDB(id={self.userInDB_ID!r}, user_ID={self.user_ID!r}, pw={self.hashed_password!r})"
'''

async def dbGetUsers():
    print('inside get all users')
    engine = create_engine('sqlite:///' + os.environ.get('APP_DB_URL'))
    conn = engine.connect()
    stmt = select(User)
    result =  conn.execute(stmt)
    conn.close()
    users = []
    print(result)
    for item in result:
        users.append({
        "user_ID": item.user_ID,
        "username": item.username,
        "email": item.email,
        "first_name": item.first_name,
        "last_name": item.last_name,
        "disabled": item.disabled, 
        "hashed_password": item.hashed_password,
        "created_at": item.created_at
    })

    print(users)   
    #return {"users": ar}
    return users
    


async def dbGetUserByUsername(username: str):
    print('inside db user by username')
    print(username)
    engine = create_engine(os.environ.get('APP_DB_URL'))
    conn = engine.connect()
    stmt = select(User).where(User.username == username)
    print(stmt)
    output = conn.execute(stmt)
    result = output.fetchone()
    conn.close()
    out = {
        "user_ID": result.user_ID,
        "username": result.username,
        "email": result.email,
        "first_name": result.first_name,
        "last_name": result.last_name,
        "disabled": result.disabled, 
        "hashed_password": result.hashed_password,
        "created_at": result.created_at
    }
    print('result of dbGetUserByUsername: ', out)
    return out

