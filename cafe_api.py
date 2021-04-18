import json

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

BaseORM = declarative_base()


class Cafe(BaseORM):
    __tablename__ = 'cafe'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)
    map_url = Column(String(500), nullable=False)
    img_url = Column(String(500), nullable=False)
    location = Column(String(250), nullable=False)
    has_sockets = Column(Boolean, nullable=False)
    has_toilet = Column(Boolean, nullable=False)
    has_wifi = Column(Boolean, nullable=False)
    can_take_calls = Column(Boolean, nullable=False)
    seats = Column(String(250))
    coffee_price = Column(String(250))
    city = Column(String(250))


def get_cafes(db_session, c_id=0, city=None):
    if c_id != 0:
        cafes = [db_session.query(Cafe).get(c_id)]
    elif city is not None:
        cafes = db_session.query(Cafe).filter(Cafe.city == city)
    else:
        cafes = db_session.query(Cafe).all()
    return [serialize_cafe(cafe) for cafe in cafes]


def add_cafe(db_session, cafe_data):
    new_cafe = Cafe()
    new_cafe.name = cafe_data['name']
    new_cafe.map_url = cafe_data['map_url']
    new_cafe.img_url = cafe_data['img_url']
    new_cafe.location = cafe_data['location']
    new_cafe.seats = cafe_data['seats']
    new_cafe.coffee_price = cafe_data['coffee_price']
    new_cafe.city = cafe_data['city']

    has_sockets = cafe_data.get('has_sockets')
    if has_sockets == 'y':
        new_cafe.has_sockets = True
    else:
        new_cafe.has_sockets = False

    has_toilet = cafe_data.get('has_toilet')
    if has_toilet == 'y':
        new_cafe.has_toilet = True
    else:
        new_cafe.has_toilet = False

    has_wifi = cafe_data.get('has_wifi')
    if has_wifi == 'y':
        new_cafe.has_wifi = True
    else:
        new_cafe.has_wifi = False

    can_take_calls = cafe_data.get('can_take_calls')
    if can_take_calls == 'y':
        new_cafe.can_take_calls = True
    else:
        new_cafe.can_take_calls = False

    db_session.add(new_cafe)
    db_session.commit()


def get_cities(db_session):
    cities = db_session.query(Cafe.city).distinct().all()
    return [y[0] for y in cities]


def serialize_cafe(cafe):
    return {
        'id': cafe.id,
        'name': cafe.name,
        'map_url': cafe.map_url,
        'img_url': cafe.img_url,
        'location': cafe.location,
        'has_sockets': cafe.has_sockets,
        'has_toilet': cafe.has_toilet,
        'has_wifi': cafe.has_wifi,
        'can_take_calls': cafe.can_take_calls,
        'seats': cafe.seats,
        'coffee_price': cafe.coffee_price,
        'city': cafe.city,
    }