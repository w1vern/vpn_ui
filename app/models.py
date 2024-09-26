from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, index=True)
    hashed_password = Column(String)
    telegram_id = Column(Integer, unique=True, index=True)
    
    
