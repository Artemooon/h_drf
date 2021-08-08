## Game API 
### Setup
___

Create a virtual environment to install dependencies in and activate it:
```
virtualenv .venv
source venv/bin/activate
```
Then install the dependencies:
```
(venv)$ pip install -r requirements.txt
```
Once pip has finished downloading the dependencies:
```
(venv)$ cd games
(venv)$ python manage.py migrate
(venv)$ python manage.py runserver
```
Navigate for swagger [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/) 
Also there are redoc [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/) 
