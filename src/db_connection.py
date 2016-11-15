import csv, hashlib, json
from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Site(Base):
    '''
    ORM class to representing site entries.
    '''
    __tablename__ = 'sites'

    id = Column(Integer,primary_key=True, autoincrement=True)
    url = Column(String(40)) 
    predicted_category = Column(String(20))
    category = Column(String(20))

    def __repr__(self):
        return '[Site:] {}\n[Category:] {}\n==============='.format(self.url, self.category)

    def __str__(self):
        return self.__repr__()

class Word(Base):
    '''
    ORM class to representing site entries.
    '''
    __tablename__ = 'words'

    id = Column(Integer,primary_key=True, autoincrement=True)
    word = Column(String(30))

    def __repr__(self):
        return self.word

    def __str__(self):
        return self.__repr__()

        

class Containment(Base):
    '''
    ORM class to representing site entries.
    '''
    __tablename__ = 'contaiment'

    id = Column(Integer,primary_key=True, autoincrement=True)
    site_id = Column(Integer, ForeignKey('sites.id'), autoincrement=True)
    word_id = Column(Integer, ForeignKey('words.id'), autoincrement=True)
    
    count = Column(Integer)

    def __repr__(self):
        return '[Word no:] {}\n[Site no:] {}\n[Count:] {}\n==============='.format(self.word_id, self.site_id, self.count)

    def __str__(self):
        return self.__repr__()

''' TEST
engine = create_engine('sqlite:///..\\db\\ranking.db', echo = False)
Base.metadata.create_all(engine, checkfirst=True)
Session = sessionmaker(bind=engine)
session = Session()
t = session.query(Site)
for i in t:
    print(i)