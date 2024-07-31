from microskel.service_template import ServiceTemplate
import events_module

class EventsService(ServiceTemplate):
    def __init__(self, name):
        super().__init__(name)

    #def get_modules(self):
    #     return super().get_modules()  # + [key_value_module.KeyV]

    def get_python_modules(self):
        return super().get_python_modules() + [events_module]


if __name__ == '__main__':
    EventsService('events_service').start()

#
#
#
#
# from flask import Flask, render_template, request
# from flask_session import Session
# from flask_restful import Api, Resource
#
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import *
#
# import json
# import os
# import logging
# import datetime
# import time
#
# app = Flask('events')
#
# db_user = os.environ.get('DB_USER') or 'event'
# db_pass = os.environ.get('DB_PASSWORD') or 'abc123'
# db_host = os.environ.get('DB_HOST') or '127.0.0.1' # cu localhoast prin file daca pun 127.0.0.1 incearca prin TCP
# db_name = os.environ.get('DB_NAME') or 'events'
# PORT = int(os.environ.get('PORT') or 5000)
# HOST = os.environ.get('HOST') or '0.0.0.0' # aici nu vreau sa zic 127.0.0.1 pentru ca v-a asculta doar pe interfata de lopback a containerului si alt container nu se poate lega la mine
# # 0.0.0.0 inseamna asculta pe toate containerele pe care le ai (loopback si outside interface)
#
# db_url = f'mysql://{db_user}:{db_pass}@{db_host}/citybreak'
#
# app.config['SQLALCHEMY_DATABASE_URI'] = db_url
#
# file_handler = logging.FileHandler('events.log')
# app.logger.addHandler(file_handler)
# app.logger.setLevel(logging.INFO)
#
# time.sleep(20)
# api = Api(app)
# db = SQLAlchemy(app)
#
# class Events(Resource):
#     def get(self):
#         city = request.args.get('city')
#         date = request.args.get('date')
#         events = db.session.query(Event)
#
#         if city:
#             events = events.filter(Event.city.like(city)).all()
#         if date:
#             events = events.filter(Event.date == date).all()
#         return [e.to_dict() for e in events], 200
#
#     def post(self):
#         city = request.form.get('city', 'Brasov')
#         name = request.form.get('name')
#         description = request.form.get('description')
#         date = request.form.get('date')
#         date = datetime.date(*[int(s) for s in date.split('-')]) if date else datetime.date.today()
#
#         event = Event(city=city, name=name, description=description, date=date)
#         db.session.add(event)
#         db.session.commit()
#         return  event.id, 201
#
#     def put(self):
#         event_id = request.form.get('id')
#
#         if not event_id:
#             return 'EVENT ID MISSING', 401
#         try:
#             event_id = int(event_id)
#         except ValueError:
#             return 'EVENT ID INVALID', 401 #TODO ceva
#         city = request.form.get('city')
#         name = request.form.get('name')
#         description = request.form.get('description')
#         date = request.form.get('date')
#         date = datetime.date(*[int(s) for s in date.split('-')]) if date else None
#
#         event = db.session.query(Event).filter(Event.id == event_id)
#
#         if event:
#             event = event.first()
#             event.city = city if city else event.city
#             event.name = name if name else event.name
#             event.description = description if description else event.description
#             event.date = date
#
#             db.session.commit()
#             return 'OK', 201
#
#         return 'Not foud', 404
#
#     def delete(self):
#         pass
#
# api.add_resource(Events, '/events')
#
# class Event(db.Model):
#     __tablename__ = 'events'
#
#     id = db.Column(db.Integer, primary_key=True)
#     city = db.Column(db.String(128)) #varchar
#     name = db.Column(db.String(256))
#     date = db.Column(db.Date)
#     description = db.Column(db.Text())
#
#     def to_dict(self):
#         d = {}
#         for k, v in self.__dict__.items():
#             if k == 'date' and v is not None:
#                 d[k] = v.strftime('%Y-%m-%d')  # Format the date as a string
#             elif '_sa_instance_state' not in k:
#                 d[k] = v
#         return d
#
# with app.app_context():
#     db.create_all()
#
# if __name__ == '__main__':
#     app.run(host=HOST, port=PORT, debug=True)