from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

_session = None

def obtain_db_session():
	global _session
	if _session != None:
		return _session
	engine = create_engine('sqlite:///restaurantmenu.db')
	Base.metadata.bind = engine
	DBSession = sessionmaker(bind=engine)
	_session = DBSession()
	return _session

def get_restaurants(session = obtain_db_session()):
	return session.query(Restaurant).order_by(Restaurant.name).all()

def get_restaurant(id, session = obtain_db_session()):
	return session.query(Restaurant).filter_by(id = id).one()

def add_restaurant(name, session = obtain_db_session()):
	restaurant = Restaurant(name = name)
	session.add(restaurant)
	return session.commit()

def update_restaurant(id, name, session = obtain_db_session()):
	restaurant = get_restaurant(id)
	restaurant.name = name
	session.add(restaurant)
	return session.commit()

def remove_restaurant(id, session = obtain_db_session()):
	restaurant = get_restaurant(id)
	session.delete(restaurant)
	return session.commit()
