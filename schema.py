
"""
GraphQL Schema Definition
Defines the GraphQL types and queries for bank branch data.

This file creates the GraphQL API layer on top of our database models.
It allows users to query bank and branch information in flexible ways.

""".


import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import Bank as BankModel, Branch as BranchModel


# GraphQL Types
class Bank(SQLAlchemyObjectType):
    """Bank GraphQL Type"""
    class Meta:
        model = BankModel
        interfaces = (relay.Node,)

class Branch(SQLAlchemyObjectType):
    """Branch GraphQL Type with bank relationship"""
    class Meta:
        model = BranchModel
        interfaces = (relay.Node,)

# Query Root
class Query(graphene.ObjectType):
    """Root Query with all available queries"""
    
    node = relay.Node.Field()
    
    # Query all branches with pagination support
    branches = SQLAlchemyConnectionField(
        Branch.connection,
        description="Get all bank branches with their bank details"
    )
    
    # Query all banks
    banks = SQLAlchemyConnectionField(
        Bank.connection,
        description="Get all banks"
    )
    
    # Query single branch by IFSC
    branch_by_ifsc = graphene.Field(
        Branch,
        ifsc=graphene.String(required=True),
        description="Get a specific branch by IFSC code"
    )
    
    # Query branches by bank name
    branches_by_bank = graphene.List(
        Branch,
        bank_name=graphene.String(required=True),
        description="Get all branches of a specific bank"
    )
    
    def resolve_branch_by_ifsc(self, info, ifsc_code):
        """Resolve single branch by IFSC code"""
        return BranchModel.query.filter_by(ifsc=ifsc).first()
    
    def resolve_branches_by_bank(self, info, bank_name):
        """Resolve branches by bank name"""
        # First find the bank by name
bank = BankModel.query.filter_by(name=bank_name).first()

# If bank exists, get all its branches
if bank:
    return BranchModel.query.filter_by(bank_id=bank.id).all()
return []  # Return empty list if bank not found

# Create schema
schema = graphene.Schema(query=Query)
