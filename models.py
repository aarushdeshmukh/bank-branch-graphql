"""
Database Models
SQLAlchemy models for Bank and Branch entities.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Bank(Base):
    """Bank model representing a banking institution"""
    __tablename__ = 'banks'

    # Primary key for the bank
    
    id = Column(Integer, primary_key=True)

    # Bank name - max 49 characters based on data 

    name = Column(String(49), nullable=False)
    
    # Relationship: One bank has many branches
    # This allows us to query bank.branches to get all branches

    branches = relationship('Branch', back_populates='bank')
    
    def __repr__(self):
        return f"<Bank(id={self.id}, name='{self.name}')>"

class Branch(Base):
    """Branch model representing a bank branch"""
    __tablename__ = 'branches'
    
    # IFSC code is unique code given to each bank to identify it fast 
    ifsc = Column(String(11), primary_key=True)
    # IS a foreign key linking to parent bank 
    bank_id = Column(Integer, ForeignKey('banks.id'), nullable=False)
    # Branch name and location
    branch = Column(String(74), nullable=False)

# Address details - made optional since not all branches have complete data
    address = Column(String(195))
    city = Column(String(50))
    district = Column(String(50))
    state = Column(String(50))
    
    # Many-to-one relationship: many branches belong to one bank
    # This lets us query branch.bank to get the parent bank details
    bank = relationship('Bank', back_populates='branches')
    
    def __repr__(self):
        return f"<Branch(ifsc='{self.ifsc}', branch='{self.branch}')>"
