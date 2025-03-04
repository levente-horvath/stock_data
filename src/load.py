from sqlalchemy import create_engine
import pandas as pd
import sys
from utils import setup_logger
from sqlalchemy.sql import text
import json

logger = setup_logger(__name__)

def load_data(ticker="unknown", file_name="transform_data.csv"):
    try:
        df = pd.read_csv(file_name, sep=',')
        return df
    except FileNotFoundError as fnf_error:
        logger.error(f"File not found: {fnf_error}")
        sys.exit(1)
    except Exception as err:
        logger.error(f"An error occurred: {err}")
        sys.exit(1)

def load_metadata(file_name="data.meta.json"):
    try:
        with open(file_name, 'r') as f:
            metadata = json.load(f)
        return metadata
    except FileNotFoundError as fnf_error:
        logger.error(f"File not found: {fnf_error}")
        sys.exit(1)
    except json.JSONDecodeError as json_error:
        logger.error(f"JSON decode error: {json_error}")
        sys.exit(1)
    except Exception as err:
        logger.error(f"An error occurred: {err}")
        sys.exit(1)


ticker = load_metadata()[0]


username = "lev"
password = "12"
host = "localhost"
port = "5432"
db = "stocks"

engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{db}')


with engine.connect() as connection:
    result = connection.execute(text("SELECT value FROM tickers WHERE value = :ticker"), {'ticker': ticker})
    
    if result.fetchone() is None:
       connection.execute(text("INSERT INTO tickers (value) VALUES (:ticker)"), {'ticker': ticker})
       connection.commit()
       

df = load_data(ticker=ticker)

df.to_sql(
    'stocks',               # Table name
    engine,                
    if_exists='replace',    # Options: 'fail', 'replace', 'append'
    index=True,           
    method='multi'        
)