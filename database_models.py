from sqlalchemy import Column,Integer,String,Float
from sqlalchemy.ext.declarative import declarative_base
base = declarative_base()
class Bank(base):
    __tablename__ = "bank_details"
    id = Column(Integer,primary_key = True, index = True)
    account_holder = Column(String, index = True)
    account_type = Column(String)
    balance = Column(Float)