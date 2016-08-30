from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from puppies import Puppy, Shelter, Base
from datetime import date
from dateutil.relativedelta import relativedelta
from sqlalchemy import func

engine = create_engine("sqlite:///puppyshelter.db")
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

#Queries

#1. Query all of the puppies and return the results in ascending alphabetical order

puppies = session.query(Puppy).order_by(Puppy.name.asc())

for puppy in puppies:
	print puppy.name

print "\n"

#2. Query all of the puppies that are less than 6 months old organized by the youngest first

limitDate = date.today() + relativedelta(months = -6)
dateStr = str(limitDate)

puppies = session.query(Puppy).filter(Puppy.dateOfBirth >= dateStr).order_by(Puppy.dateOfBirth.desc())

for puppy in puppies:
	print puppy.dateOfBirth

print "\n"

#3. Query all puppies by ascending weight

puppies = session.query(Puppy).order_by(Puppy.weight.asc())

for puppy in puppies:
	print puppy.weight

print "\n"

#4. Query all puppies grouped by the shelter in which they are staying

shelters = session.query(Shelter, func.count(Puppy.id)).join(Puppy).group_by(Shelter.id)

for shelter in shelters:
	print str(shelter)

print "\n"

