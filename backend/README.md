## Get it going

### start the venv
-> folder backend
```python
source myvenv/bin/activate
```
## run the backend server 
```python
fastapi dev main.py
```
## open api docs
http://localhost:8000/docs

## run a test - in backend dir
```python 
python -m test.modelTest
```

## you need an .env file for this to work
containing
```
APP_DB_URL=sqlite:///appDB/app.db
```

