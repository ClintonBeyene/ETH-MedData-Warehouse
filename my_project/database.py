from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# Fetch database connection parameters from environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", 5432)
DB_NAME = os.getenv("DB_NAME", "ETH-MedData-Warehouse")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")

engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')
Sessions = sessionmaker(bind=engine)

Base = declarative_base()

def get_db():
    db = Sessions()
    try:
        yield db
    finally:
        db.close()