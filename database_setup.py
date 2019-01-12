import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Studio(Base):
	__tablename__ = 'studio'
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	founded_date = Column(String(10))
	founder = Column(String(30))

	# Returning object in easily serializeable format for JSON
	@property
	def serialize(self):
		return {
		'name':self.name,
		'id':self.id,
		'founded_date':self.founded_date,
		'founder':self.founder,
		}

class Game(Base):
	__tablename__ = 'game'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	description = Column(String(250))
	release_date = Column(String(10))
	quantity = Column(Integer)
	price = Column(String(8))

	# Relational mapping
	studio_id = Column(Integer, ForeignKey('studio.id'))
	studio = relationship(Studio)

	@property
	def serialize(self):
		return {
		'name': self.name,
		'id':self.id,
		'description':self.description,
		'release_date':self.release_date,
		'quantity':self.quantity,
		'price':self.price,
		}
	


