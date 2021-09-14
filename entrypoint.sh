

cd games

python manage.py migrate --no-input
python manage.py collectstatic --no-input

#gunicorn  games.wsgi:application --bind :8000
