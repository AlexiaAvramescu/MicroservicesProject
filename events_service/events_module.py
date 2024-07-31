from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import *
from sqlalchemy import *
import datetime

from microskel.db_module import Base


class EventsModule(Base):  # ORM - Oject - Relational Mapping
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    city = Column(String(128))  # varchar
    name = Column(String(256))
    date = Column(Date)
    description = Column(Text())

    def __init__(self, city, name, date, description):
        self.city = city
        self.name = name
        self.date = date
        self.description = description

    def to_dict(self):
         d = {}
         for k, v in self.__dict__.items():
             if k == 'date' and v is not None:
                 d[k] = v.strftime('%Y-%m-%d')  # Format the date as a string
             elif '_sa_instance_state' not in k:
                 d[k] = v
         return d

def configure_views(app):
    @app.route('/events/<city>/<date>', methods=['GET'])
    def events(city, date, db: SQLAlchemy):
        events = db.session.query(EventsModule)

        if city:
            events = events.filter(EventsModule.city.like(city))
        if date:
            events = events.filter(EventsModule.date == date)
        return [e.to_dict() for e in events], 200

    @app.route('/events', methods=['POST'])
    def create(request: Request, db: SQLAlchemy):
        ev = EventsModule(
            city=request.form.get('city'),
            name=request.form.get('name'),
            date=request.form.get('date'),
            description=request.form.get('description'))
        db.session.add(ev)
        db.session.commit()
        return jsonify(ev.id), 201

    @app.route('/events', methods=['PUT'])
    def modify(request: Request, db: SQLAlchemy):
        event_id = request.form.get('id')

        if not event_id:
            return 'EVENT ID MISSING', 401
        try:
            event_id = int(event_id)
        except ValueError:
            return 'EVENT ID INVALID', 401  # TODO ceva
        city = request.form.get('city')
        name = request.form.get('name')
        description = request.form.get('description')
        date = request.form.get('date')
        date = datetime.date(*[int(s) for s in date.split('-')]) if date else None

        event = db.session.query(EventsModule).filter(EventsModule.id == event_id)

        if event:
            event = event.first()
            event.city = city if city else event.city
            event.name = name if name else event.name
            event.description = description if description else event.description
            event.date = date

            db.session.commit()
            return 'OK', 201

        return 'Not foud', 404

    @app.route('/events', methods=['DELETE'])
    def delete(request: Request, db: SQLAlchemy):
        pass
