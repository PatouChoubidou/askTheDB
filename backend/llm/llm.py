from langchain_community.llms import Ollama
# from langchain_community import SQLDatabase
from langchain_community.utilities.sql_database import SQLDatabase
from langchain.chains import create_sql_query_chain
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, text
import backend.db.testCompany_tableInfos as testCompany_tableInfos
import datetime 
import re
import sqlite3
import os
from dotenv import load_dotenv, find_dotenv

# use env
load_dotenv(find_dotenv())

# vars

model_name = os.environ.get('MODEL_NAME')
db = SQLDatabase.from_uri("sqlite:///db/testCompany.db")
 
async def getDBTables():
    db_tables = db.get_usable_table_names()
    table_string = ', '.join(map(str, db_tables))
    return {"tables": table_string}


async def getSQLiteCreateStmts():
    """
        use this func to get all table create stmts as array of strings
        hopefully use to make the database graph view in frontend
    """
    arr = []
    try:
        con = sqlite3.connect("db/testCompany.db")
        cursor = con.cursor()
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
        result = cursor.fetchall()

        for tupple in result:
            newDic = {"stmt": ""}
            for item in tupple:
                if type(item) is str:
                    newDic["stmt"] = item
                    arr.append(newDic)

        cursor.close()
        con.close()
    except:
        print('blub')
    arr.pop(0)
    return arr


async def getSQLiteCreateStatementsString():
    resultStr = ""
    try:
        con = sqlite3.connect("db/testCompany.db")
        cursor = con.cursor()
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
        result = cursor.fetchall()
        
        resultStr += """These SQL create table statements help you to understand
                    all the tables of the database and the existing associated columns: \n"""

        for tupple in result:
            for item in tupple:
                if type(item) is str:
                    resultStr += item 
                    resultStr += "\n"

        cursor.close()
        con.close()
    except:
        print('blub')
    return resultStr


async def getColumnNames(query):
    # this is the sqlite solution - would not work for other dbs
    columns = []
    query = ' '.join(query.splitlines())
    try:
        conn = sqlite3.connect("db/testCompany.db")
        cursor = conn.cursor()
        res = cursor.execute(query)
        columns = [description[0] for description in cursor.description]
        print(columns)
        conn.close()
    except: 
        'something wrong again'
    return columns
    

# run an sql statement against the db given with check
async def run_the_SQL(sql_stmt, db):
    if sql_write_access_check(sql_stmt):
        db_reply = await db_run_question(sql_stmt, db)
    else:
        db_reply = "You are not allowed to alter the database. Please try again."
    if db_reply == '':
        db_reply = '-'
    return db_reply


# run an sql statement against the db given
async def db_run_question(generatedSQLQuery, db): 
    try: 
        print('generated Query inside run question:', generatedSQLQuery)
        answer = db.run(generatedSQLQuery)
        print(answer)
    except SQLAlchemyError as e:
        answer = str(e.__dict__['orig'])
    except:
        answer = "the database could not process the generated sql"
    return answer


# check wheater sql statement is insert update delete etc
'''
def sql_write_access_check(generatedSQLQuery): 
    sql_write_indicator = ['INSERT', 'CREATE', 'DELETE', 'UPDATE', 'DROP TABLE', 'ALTER TABLE', PRAGMA ]
        
    for indicator in sql_write_indicator:
        if generatedSQLQuery.startswith(indicator):
            return False
    return True
'''
# a little less secure but 
# if you wanna allow certain db alterations use the upper version
def sql_write_access_check(generatedSQLQuery): 
    if(generatedSQLQuery.lower().startswith('select') or 
       generatedSQLQuery.lower().startswith('\nselect')):
        return True
    return False


# ask the llm to generate an sql statement
async def generate_SQL(question, db, table_infos, max_k): 
    
    # unfortunately not working the following is not working
    # The ouput is printable but it messes with the llm ?
    # context = await db.get_context()    
    # table_names = context['table_names']
    # table_infos = context['table_info']
    
    # my own funcs
    tables = await getDBTables()
    table_names = tables['tables']

    max_k = 'ten'
    db_dialect = db.dialect

    prompt = """
        You are a professional in {db_dialect} databases. 
        Given a database with these tables known: {table_names}.
        Form a syntactically correct sql query out of the {question}.
        Refine the query this information about the tables {table_infos}.
        Limit the result to replies to a maximum of {max_k}. 
        Be careful to not query for columns that do not exist. 
        No explanation. Output just the query. 
        Be careful not to put the word 'sql', nor any symbols like quotes, backticks or this symbol: '`' in your answer!
        """
    
    input = [db_dialect, table_names, question, table_infos, max_k]
    llm = Ollama(model=model_name, system=prompt, temperature=0.9)
    generatedSQLQuery = llm.invoke(input)
    # strip any backticks, sanitize output
    generatedSQLQuery=re.sub("sql","",generatedSQLQuery)
    generatedSQLQuery=re.sub(r"[\`]","",generatedSQLQuery)
    # generatedSQLQuery = generatedSQLQuery.replace('\n', '')
    return generatedSQLQuery


# ask the llm to explain an sql statement by a given question
async def explainSQL(db, question, db_reply):
    tables = await getDBTables()
    table_names = tables['tables'] or ''
    table_infos = await getSQLiteCreateStatementsString() or testCompany_tableInfos.tables_create_stmts 
    db_dialect = db.dialect
    out = ""
    if(db_reply != ''):
        
        prompt2 = """
        Format the output of a {db_dialect} database.
        The database has these tables: {table_names}. 
        Use this information on questions concerning the structure of the database: {table_infos}.
        Given a question {question} and the database reply {db_reply},
        form a human readable answer without any extra information or explanation.
        Do not order responses alphabetically.
        Do not generate any sql statements or try to contact the database.
        If the reply is empty say that the reply is empty and be careful not to make up an answer based on the question.
        Format lists or arrays as enumeration.
        If the reply says: 'You are not allowed to alter the database. Please try again', just repeat the sentence.
        """

        llm = Ollama(model=model_name, system=prompt2, temperature=0.1)
        input2 = [db_dialect, table_names, question, db_reply]
        explanation = llm.invoke(input2)
        out = explanation
    else: 
        out = 'The database did not reply. Maybe recheck the query?'
    return out


# process chain: take a question, generate sql, run sql, explain sql
async def askTheLLM(question):
    print('Here is the question: '+ question)
    print('The LLM tries to ask the db...')

    # python dic
    output = {
        "question" : "",
        "sql": "",
        "column_names": "",
        "db_response": "-",
        "explanation": ""
    }
    
    # my own table create stmts 
    table_infos = await getSQLiteCreateStatementsString() or testCompany_tableInfos.tables_create_stmts
    now = datetime.datetime.now()
    current_date_str = '' + str(now.year) + '-' + str(now.month) + '-' + str(now.day)
    max_k = '10' 
    output['question'] = question

    # generate the sql 
    generatedSQLQuery = await generate_SQL(question, db, table_infos, max_k)
    output['sql'] = generatedSQLQuery

    # get the column names then run the sql
    column_names_as_string = await getColumnNames(generatedSQLQuery)
    output["column_names"] = column_names_as_string
    db_reply = await run_the_SQL(generatedSQLQuery, db)
    output['db_response'] = db_reply 

    print(output)

    #explain the sql 
    output["explanation"] = await explainSQL(db, question, db_reply)
    
    return output


# process chain: run sql, explain sql
async def runSQLandExplain(sql, question):
    print('Here ist the question: '+ question)
    print('The LLM tries to ask the db...')

    # python dic
    output = {
        "question" : question,
        "sql": sql,
        "column_names": "",
        "db_response": "-",
        "explanation": ""
    }
   
    # run the sql
    column_names = await getColumnNames(sql) or []
    print(column_names)
    output["column_names"] = column_names or ''
    db_reply = await run_the_SQL(sql, db)
    output['db_response'] = db_reply 

    #explain the sql 
    output["explanation"] = await explainSQL(db, question, db_reply)
    return output