import os
import psycopg2
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt

load_dotenv()

# Fetch database connection parameters from environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", 5432)
DB_NAME = os.getenv("DB_NAME", "ETH-MedData-Warehouse")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Create the engine
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

class DbConn:
    def __init__(self):
        try:
            # Establish a connection to the database
            self.conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            print("Connected to database")
        except Exception as e:
            print(f"An error occurred: {e}")

    def insert_data(self, Channel_Title, Channel_Username, ID, Message, Date, Media_Path):
        try:
            cur = self.conn.cursor()
            query = """
                INSERT INTO RawData (Channel_Title, Channel_Username, ID, Message, Date, Media_Path) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cur.execute(query, (Channel_Title, Channel_Username, ID, Message, Date, Media_Path))
            self.conn.commit()
            cur.close()
            self.conn.close()
        except Exception as e:
            print("Error: ", e)

    def read_data(self, table_name: str) -> pd.DataFrame:
        try:
            # Load data using pandas
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", self.conn)
            self.conn.close()
            return df
        except Exception as e:
            print("Error reading data:", e)
            raise

    def save_df_to_postgres(self, df, table_name):
        try:
            # Create an engine instance
            engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

            # Save DataFrame to PostgreSQL
            df.to_sql(table_name, engine, if_exists='replace', index=False)
        except Exception as e:
            print("Error saving data:", e)

class DatabaseConn:
    def __init__(self):      
        try:
            # Create an engine instance
            self.engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
            print("Connected to database using SQLAlchemy")
        except Exception as e:
            print("Error connecting to database using SQLAlchemy:", e)
            raise

    def insert_dataframe_data(self, table_name: str, data: pd.DataFrame):
        try:
            # Save DataFrame to PostgreSQL
            data.to_sql(table_name, self.engine, if_exists='replace', index=False)
        except Exception as e:
            print("Error saving data:", e)