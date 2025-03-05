from sqlalchemy import create_engine
import pandas as pd
import sys
from utils import setup_logger
from sqlalchemy.sql import text
import json
from airflow.models.dag import DAG
from airflow.decorators import task
from airflow.utils.task_group import TaskGroup
from airflow.hooks.base import BaseHook
import extract
import transform
from datetime import datetime

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


def main():
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


@task
def load_task():
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

if __name__ == "__name__":
    main()



# Starting how_to_task_group
with DAG(dag_id="stock_etl", schedule="0 9 * * *", start_date=datetime(2025, 3, 1), catchup=False) as dag:
    with TaskGroup("extract_data", tooltip="Extract the data") as extract_src:
        extract_src = extract.extract_task()
    
    with TaskGroup("transform_data", tooltip="Transform the data") as transform_src:
        transform_src = transform.transform_task()


    with TaskGroup("load_data", tooltip="Load the data") as load_src:
        load_src = load_task()
    
    extract_src >> transform_src >> load_src
