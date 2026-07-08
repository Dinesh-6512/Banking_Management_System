from pydantic import BaseModel
class Bank(BaseModel):          
    account_holder : str          
    account_type : str  
    balance : float   