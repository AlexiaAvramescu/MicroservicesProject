import json

from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import *
from sqlalchemy import *
import redis
from decouple import config

from microskel.db_module import Base
client = redis.Redis(host=config('REDIS_HOST', 'redis'), port=6379, db=0, decode_responses=True)

def configure_views(app):
    @app.route('/weather/<city>/<date>', methods=['GET'])
    def get_weather(city: str, date: str):
        key = f'{city}-{date}' if date else city
        weather = client.get(key)
        print(f'key={key}')
        if not weather:
            return 'No data', 401
        print(f'weather = {weather}')
        weather = client.get(key).encode('utf-8')
        weather = json.loads(weather)
        return weather, 200

    @app.route('/weather', methods=['POST'])
    def create_weather(request: Request):
        keys = ('temerature', 'humidity', 'wind')
        weather = {k: request.form.get(k) for k in keys}
        city = request.form.get('city', 'Brasov')
        date = request.form.get('date', '')
        key = f'{city}-{date}' if date else city
        client.set(key, json.dumps(weather))

        return 'OK', 200