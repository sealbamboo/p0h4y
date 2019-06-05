from sqlalchemy import Column, Integer, String, Date
from .database import Base

class Dataset(Base):
    __tablename__ = 'dataset'
    index = Column(Integer, primary_key=True)
    tweetid = Column('tweetid',Integer)
    date = Column('date',Date)
    tweetcontent = Column('tweetcontent',String)
    url = Column('url',String)

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