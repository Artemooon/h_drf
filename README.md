## Game API 
### Setup
___

The first thing to do is to clone the repository:

```
git clone https://github.com/Artemooon/h_drf.git
cd h_drf
```
Create a virtual environment to install dependencies in and activate it:
```
virtualenv .venv
source venv/bin/activate
```
Then install the dependencies:
```
(venv)$ pip install -r requirements.txt
```
Create __.env__ file and grab data from __.env.dist__ with own filling

Once pip has finished downloading the dependencies:
```
(venv)$ cd games
(venv)$ python manage.py migrate
(venv)$ python manage.py runserver 8000
```
Navigate for swagger [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/) 

Also there are redoc [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/) 
