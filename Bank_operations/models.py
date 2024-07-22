from sqlalchemy import Integer,String,Float,Column
from database import Base

class Account(Base):
    __tablename__ = "Account Holder Details"
    
    id = Column(Integer,primary_key = True, index = True)
    name = Column(String)
    balance = Column(Float)
    account_type = Column(String)
    
    