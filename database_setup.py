#!/usr/bin/python3
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Catalog(Base):
    __tablename__ = 'catalog'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

class Item(Base):
    __tablename__ = 'item'


    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    price = Column(String(8))
    type = Column(String(250))
    catalog_id = Column(Integer,ForeignKey('catalog.id'))
    catalog = relationship(Catalog)

#We added this serialize function to be able to send JSON objects in a serializable format
    @property
    def serialize(self):

       return {
           'name'         : self.name,
           'description'         : self.description,
           'id'         : self.id,
           'price'         : self.price,
           'type'         : self.type,
       }


engine = create_engine('sqlite:////var/www/catalog2/catalog2/catalog_database.db')


Base.metadata.create_all(engine)
