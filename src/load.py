from sqlalchemy import create_engine
import pandas as pd
import sys
from utils import setup_logger

logger = setup_logger(__name__)

username = "lev"
password = "12"
host = "localhost"
port = "5432"
db = "stocks"

engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{db}')

def load_data(file_name="transform_data.csv"):
    try:
        df = pd.read_csv(file_name, sep=',')
        return df
    except FileNotFoundError as fnf_error:
        logger.error(f"File not found: {fnf_error}")
        sys.exit(1)
    except Exception as err:
        logger.error(f"An error occurred: {err}")
        sys.exit(1)



df = load_data()


df.to_sql(
    'users',               # Table name
    engine,                # SQLAlchemy engine
    if_exists='append',    # Options: 'fail', 'replace', 'append'
    index=True,           # Do not write DataFrame index as a column
    method='multi'         # Batch insert for efficiency (optional)
)