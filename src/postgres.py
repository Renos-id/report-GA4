import os
from sqlalchemy import create_engine
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def send_to_postgres(df, table_name, append=False):
    # Get PostgreSQL connection information from environment variables
    host = os.getenv('POSTGRES_HOST')
    port = os.getenv('POSTGRES_PORT')
    database = os.getenv('POSTGRES_DATABASE')
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')

    # Create SQLAlchemy engine
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')

    # Append mode
    if append:
        df.to_sql(table_name, engine, if_exists='append', index=False)
    else:
        df.to_sql(table_name, engine, if_exists='replace', index=False)