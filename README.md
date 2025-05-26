# askTheDB
This project was part of my bachelor thesis.<br>
It contains a test dummy web app which enables the user to pose questions in natural language to a test-sqlite-database using a locally running LLM.
<br>

## Tools
### model
- ollama
- langchain

### backend
- FastAPI

### frontend 
- Vue3.js

## Requirements
Ollama running CodeGemma<br>
https://ollama.com/<br>
https://ollama.com/library<br>
using a machine with at least 8GB RAM<br>

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




