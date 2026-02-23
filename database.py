"""
Database Configuration
Handles database connection, initialization, and SQL file import.
"""

import os
import subprocess
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Get database URL from environment variable, default to SQLite for local development
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///banks.db')

# Heroku uses 'postgres://' but SQLAlchemy needs 'postgresql://'
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

# Create the database engine
engine = create_engine(DATABASE_URL, convert_unicode=True)

# Session management
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Base class for all models
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    """
    Initialize database.
    For SQLite: Downloads and imports the SQL file if database doesn't exist.
    For PostgreSQL: Assumes database is already set up.
    """
    import models
    
    if DATABASE_URL.startswith('sqlite'):
        db_path = DATABASE_URL.replace('sqlite:///', '')
        
        if not os.path.exists(db_path):
            print("Database not found. Setting up database...")
            
            sql_url = "https://raw.githubusercontent.com/Amanskywalker/indian_banks/master/indian_banks.sql"
            sql_file = "indian_banks.sql"
            
            print(f"Downloading database from {sql_url}...")
            subprocess.run(['curl', '-o', sql_file, sql_url], check=True)
            
            print("Importing data into database...")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Drop tables if they exist to avoid conflicts
            cursor.execute("DROP TABLE IF EXISTS branches")
            cursor.execute("DROP TABLE IF EXISTS banks")
            
            # Read and execute SQL file
            with open(sql_file, 'r', encoding='utf-8') as f:
                sql_script = f.read()
                cursor.executescript(sql_script)
            
            conn.commit()
            conn.close()
            
            os.remove(sql_file)
            print("✅ Database ready!")
    else:
        Base.metadata.create_all(bind=engine)

def shutdown_session(exception=None):
    """Clean up database session"""
    db_session.remove()
