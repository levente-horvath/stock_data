import json
from utils import setup_logger
import yfinance as yf
from datetime import datetime, timedelta
from utils import setup_logger
from airflow.decorators import task
from airflow.utils.task_group import TaskGroup
from airflow.hooks.base import BaseHook


# Initialize setup logger
logger = setup_logger(__name__)



# Returns a the daily stock price up to today
# Ticker -> Stock symbol
# Duration -> In days
def get_stock_price_today(ticker, duration):

    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=duration)).strftime('%Y-%m-%d')

    return yf.download(ticker, start=start_date, end=end_date)


# Return stock price for specicific
# Ticker -> Stock symbol
# date -> Year-Month-Day
def get_stock_price_with_specific_date(ticker, start_date, end_date):
    return yf.download(ticker, start=start_date, end=end_date)


@task
def extract_task():
    data = get_stock_price_today("AMZN", 365)

    filename = "stockprices.csv"
    data.to_csv(filename)

    logger.info(f"Data saved to {filename}")


def main():

    data = get_stock_price_today("AMZN", 365)

    filename = "stockprices.csv"
    data.to_csv(filename)

    logger.info(f"Data saved to {filename}")

if __name__ == "__main__":
    main()
