from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from site_rank_global import logger, db_location

Base = declarative_base()


class Site(Base):
    '''
    ORM class to representing site entries.
    '''
    __tablename__ = 'sites'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(40))
    predicted_category = Column(String(20))
    category = Column(String(20))

    def __repr__(self):
        return '[Site:] {}\n[Category:] {}\n==============='.format(
            self.url, self.category)

    def __str__(self):
        return self.__repr__()


class Word(Base):
    '''
    ORM class to representing site entries.
    '''
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String(30))

    def __repr__(self):
        return self.word

    def __str__(self):
        return self.__repr__()


class Containment(Base):
    '''
    ORM class to representing site entries.
    '''
    __tablename__ = 'containment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    site_id = Column(Integer, ForeignKey('sites.id'), autoincrement=True)
    word_id = Column(Integer, ForeignKey('words.id'), autoincrement=True)

    count = Column(Integer)

    def __repr__(self):
        return '\n[Word no:] {}\n[Site no:] {}\n[Count:] {}\n===============\n'.format(self.word_id, self.site_id, self.count)

    def __str__(self):
        return self.__repr__()


class RankDBHandler():
    '''
    DB connection handler.
    '''

    def __init__(self):

        # Create DB engine.
        self.engine = create_engine(db_location, echo=False)

        # Generate metadata.
        Base.metadata.create_all(self.engine, checkfirst=True)

        # Create session.
        Session = sessionmaker(bind=self.engine)
        self.current_session = Session()

    def __exit__(self):
        '''
        Make sure to commit changes and close connection uppon destruction.
        '''

        self.current_session.commit()
        self.current_session.close()

    def test_connection(self):
        '''
        Returns all site.
        '''
        return [x for x in self.current_session.query(Site)]

    def update_containment(self, site, word, count=1, increment=True):
        '''
        Insert or update cointainment data.
        '''

        # Check in DB if entry exists.
        result = self.current_session.query(Containment).filter(
            Containment.site_id == site, Containment.word_id == word)

        # If exits, update counter.
        if(result.count() > 0):
            logger.info('Update entry.')

            if increment:
                result[0].count += 1
            else:
                result[0].count = count

            logger.debug(result[0])

        # Otherwise create new entry
        else:
            logger.info('Add new entry.')
            self.current_session.merge(Containment(
                site_id=site, word_id=word, count=count))
        self.current_session.commit()

    def add_word(self, word):
        '''
        Add new word to database. Returns the id of the matching entry.
        '''
        result = self.current_session.query(Word).filter(Word.word == word)

        if(result.count() == 0):
            db_word = Word(word=word)
            self.current_session.merge(db_word)
            self.current_session.commit()
        return self.current_session.query(Word).filter(Word.word == word)[0].id

    def get_site_list(self):
        """"""

        return [x.url.encode('utf-8') for x in self.current_session.query(Site)]

    def get_site_id(self, site):
        '''
        '''
        id = self.current_session.query(Site).filter(
            Site.url.ilike('%{}%'.format(site)))[0].id
        if id:
            return id
        else:
            return -1

    def get_word_id(self, word):
        '''
        '''
        id = self.current_session.query(Word).filter(Word.word == word)[0].id
        if id:
            return id
        else:
            return -1

    # def add_site(self, site):
    #     '''
    #     Add site to database. Returns the id of the matching entry.
    #     '''

    #     result = self.current_session.query(Site).filter(Site.site == site)

    #     if(result.count() == 0):
    #         db_site = Site(site=site)
    #         self.current_session.merge(db_site)
    #         self.current_session.commit()
    # return self.current_session.query(Site).filter(Site.site == site)[0].id

''' TEST
engine = create_engine('sqlite:///..\\db\\ranking.db', echo = False)
Base.metadata.create_all(engine, checkfirst=True)
Session = sessionmaker(bind=engine)
session = Session()
t = session.query(Site)
for i in t:
    print(i)
# t_handler = RankDBHandler()
# t_handler.update_containment(5, 6)
# print(t_handler.add_word('test_alma'))
# print(t_handler.add_word('test_korte'))
# print(t_handler.get_site_list())
# print(t_handler.add_site('test_site_1'))
# print(t_handler.test())
'''
