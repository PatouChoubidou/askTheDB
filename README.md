# askTheDB
This project was part of my bachelor thesis.<br>
It contains a test dummy web app which enables the user to pose questions in natural language to a test-sqlite-database using a locally running LLM.
<br>

https://github.com/user-attachments/assets/4e271ea6-3a02-40c8-9a5b-a9d55407b28e


## Tools
### model
- ollama
- langchain

### backend
- FastAPI

### frontend 
- Vue3.js

## Requirements
Download ollama and a model of your choice<br>
https://ollama.com/<br>
https://ollama.com/library<br>
Needs maybe a machine with at least 8GB RAM<br>

### install python packages
create a virtual enviroment in backend folder if not already there<br>
```python -m venv myvenv```<br>
install all packages<br>
```python3 -m pip install -r requirements.txt```

## Run it

- activate venv ```source myvenv/bin/activate```
- run ollama with your chosen model
- create .env file 
- add ```MODEL_NAME=yourmodelname``` to .env
- add ```APP_DB_URL=sqlite:///appDB/app.db``` to .env 

#### start the servers
```
cd frontend
npm run dev
```
```
cd backend
fastapi run main.py
```




