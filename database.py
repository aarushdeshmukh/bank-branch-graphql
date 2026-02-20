"""
Database Configuration
Handles database connection, initialization, and SQL file import.
"""

import os
import subprocess
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Get database URL from environment variable, default to SQLite for local development


DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///banks.db')

# Heroku uses 'postgres://' but SQLAlchemy needs 'postgresql://'
# This converts it automatically

if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

# Create the database engine - this is what actually talks to the database
engine = create_engine(DATABASE_URL, convert_unicode=True)
# Session management - allows us to query the database
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Base class for all our models
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    """
    Initialize database.
    For SQLite: Downloads and imports the SQL file if database doesn't exist.
    For PostgreSQL: Assumes database is already set up.
    """
    # Import models to register them with Base
    import models
    
    # Check if using SQLite and database doesn't exist
    if DATABASE_URL.startswith('sqlite'):
        db_path = DATABASE_URL.replace('sqlite:///', '')
        
        # Check if database file already exists
        if not os.path.exists(db_path):
            print("Database not found. Setting up database...")
            
            # Download SQL file from GitHub
            sql_url = "https://raw.githubusercontent.com/Amanskywalker/indian_banks/master/indian_banks.sql"
            sql_file = "indian_banks.sql"
            
            print(f"Downloading database from {sql_url}...")
            subprocess.run(['curl', '-o', sql_file, sql_url], check=True)
            
            # Create tables first
            Base.metadata.create_all(bind=engine)
            
            # Import SQL file into SQLite
            print("Importing data into database...")
            subprocess.run(['sqlite3', db_path, f'.read {sql_file}'], check=True)
            
            # Clean up SQL file
            os.remove(sql_file)
            print("Database setup complete!")
    else:
        # For PostgreSQL (Heroku), just create tables
        # Assumes data is already loaded or will be loaded separately
        Base.metadata.create_all(bind=engine)

def shutdown_session(exception=None):
    """Clean up database session"""
    db_session.remove()
