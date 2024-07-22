from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field, condecimal
from typing import Optional
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind = engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        
class Bank(BaseModel):
    name : str = Field(min_length=2,max_length=50, description="Enter your name")
    balance: Optional[condecimal(max_digits=10, decimal_places=3)] = Field(None, description="Your Balance is : ")
    account_type : str = Field(None, description="User's account type")
    
    
Account_holders = []

@app.get("/")
def get_details(db : Session = Depends(get_db)):
    return db.query(models.Account).all()

@app.post("/")
def create_account(account : Bank, db : Session = Depends(get_db)):
    account_model = models.Account()
    account_model.name = account.name
    account_model.balance = account.balance
    account_model.account_type = account.account_type
    db.add(account_model)
    db.commit()
    

@app.put("/", response_model=Bank)
def update_account_balance(id: int, balance: condecimal(max_digits=10, decimal_places=3), db: Session = Depends(get_db)):
    account_model = db.query(models.Account).filter(models.Account.id == id).first()
    
    if account_model is None:
        raise HTTPException(status_code=404, detail="Account not found")
    
    account_model.balance = balance
    db.commit()
    
    
        

        
    
        