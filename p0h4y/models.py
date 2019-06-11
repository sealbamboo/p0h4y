from sqlalchemy import Column, Integer, String, Date
from .database import Base

class Dataset(Base):
    __tablename__ = 'dataset'
    index           = Column(Integer, primary_key=True)
    tweetid         = Column('tweetid',Integer)
    date            = Column('date',Date)
    tweetcontent    = Column('tweetcontent',String)
    url             = Column('url',String)

    def __init__(self, tweetid, date, tweetcontent, url):
        self.tweetid        = tweetid
        self.date           = date
        self.tweetcontent   = tweetcontent
        self.url            = url

    def get_tweetid(self):
        return self.tweetid

    def get_date(self):
        return self.date

    def get_tweetcontent(self):
        return self.tweetcontent
    
    def get_url(self):
        return self.url

    # def __repr__(self):
    #     return {'tweetid': self.get_tweetid, 
    #             'date': self.get_date,
    #             'tweetcontent': self.get_tweetcontent,
    #             'url': self.get_url}

class Model(Base):
    __tablename__= 'models'
    id          = Column(Integer, primary_key=True)
    name        = Column('name',String)
    technical   = Column('technical',String)
    description = Column('description',String)
    location    = Column('location',String)
    image       = Column('image',String)

    def __init__(self, n_, t_, d_, l_, i_):
        self.name           = n_
        self.technical      = t_
        self.description    = d_
        self.location       = l_
        self.image          = i_

    def get_name(self):
        return self.name

    def get_technical(self):
        return self.technical

    def get_description(self):
        return self.description

    def get_location(self):
        return self.location

    def get_image(self):
        return self.image