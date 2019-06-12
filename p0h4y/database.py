from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql://capstone_app:capstoneapp2019@localhost/capstone_app?charset=utf8mb4",convert_unicode=True)
session = sessionmaker( autocommit=False,
                        autoflush=False,
                        bind=engine)()      # Session is a class

Base = declarative_base()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=engine)



# dataset = Dataset(3200,"123456789025","12-12-2019","Blah Blah","www.google.com.au")
# session.add(dataset)
# session.commit()

# result = [r.tweetid for r in session.query(Dataset).all()]
# from pdb import set_trace; set_trace()


# # Base connection
# def connectTable(name):
#     connection = engine.connect()
#     metadata = db.MetaData()
#     census = db.Table(name, metadata, autoload=True, autoload_with=engine)

#     return census

# def get_dataset():
#     census = connectTable('dataset')

#     # Equivalent to 'SELECT * FROM dataset'
#     query = db.select([census])

#     # Executing Query
#     ResultProxy = connection.execute(query)

#     # Fetch Data
#     ResultSet = ResultProxy.fetchall()

#     return ResultSet


# # TEST CONNECTION
# #----------------------------------------------------
# #----------------------------------------------------
# # Print the column names
# # print(census.columns.keys())

# # Print full table metadata
# # print(repr(metadata.tables['dataset']))

# #Equivalent to 'SELECT * FROM dataset'
# # query = db.select([census])
# # ResultProxy = connection.execute(query)


# # ResultSet = ResultProxy.fetchall()

# # ResultSet[:3]