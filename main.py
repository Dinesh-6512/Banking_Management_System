from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from models import Bank
from database import sessionlocal,engine
import database_models

database_models.base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

accounts = [
    Bank(id=1,account_holder="dinesh",account_type="savings",balance=45.99),
    Bank(id=2,account_holder="lokesh",account_type="salary account",balance=80.32),
    Bank(id=3,account_holder="phani",account_type="savings",balance=30.12),
    Bank(id=4,account_holder="john",account_type="salary account",balance=70.66),
]

def init_db():
    db = sessionlocal()
    existing_account = db.query(database_models.Bank).count()
    if existing_account == 0:
        for account in accounts :
            db.add(database_models.Bank(**account.model_dump()))
        db.commit()
        print("Database initialized with sample details.")      
    db.close()
init_db() 

@app.get("/")
def greet():
    return {"welcome to fastapi"}


@app.get("/accounts")
def get_all_details(db: Session = Depends(get_db)):
    account = db.query(database_models.Bank).all()
    return account

@app.get("/accounts/{account_id}")
def get_account_by_id(account_id: int, db: Session = Depends(get_db)):
    account = db.query(database_models.Bank).filter(database_models.Bank.id == account_id).first()
    if not account:
        return {"error": "details not found"}
    return account

@app.post("/accounts")
def create_account(account: Bank, db: Session = Depends(get_db)):
    db.add(database_models.Bank(**account.model_dump()))
    db.commit()
    return {"message": "account added successfully"}


@app.put("/details/{account_id}")
def update_account(account_id: int, account: Bank, db: Session = Depends(get_db)):
    db_account = db.query(database_models.Bank).filter(database_models.Bank.id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="details not found")
    db_account.account_holder = account.account_holder
    db_account.account_type = account.account_type
    db_account.balance = account.balance
    db.commit()
    db.refresh(db_account)
    return {"message": "details updated successfully"}

@app.delete("/accounts/{account_id}")
def delete_account(account_id: int, db: Session = Depends(get_db)):
    db_account = db.query(database_models.Bank).filter(database_models.Bank.id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="account not found")
    db.delete(db_account)
    db.commit()
    return {"message": "account deleted successfully"} 