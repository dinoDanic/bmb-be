from email.policy import default
from enum import unique
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class AccountTable(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hash_password = Column(String)
    active = Column(Boolean, default=True)

class OrderTable(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    
