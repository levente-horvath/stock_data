import json
from utils import setup_logger
import yfinance as yf
from datetime import datetime, timedelta
from utils import setup_logger


# Initialize setup logger
logger = setup_logger(__name__)

# Returns a the daily stock price up to today
# Ticker -> Stock symbol
# Duration -> In days
def get_stock_price_date(ticker, duration):

    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=duration)).strftime('%Y-%m-%d')

    return yf.download(ticker, start=start_date, end=end_date)



def main():

    data = get_stock_price_date("GOOG", 365)

    filename = "stockprices.csv"
    data.to_csv(filename)

    logger.info(f"Data saved to {filename}")

if __name__ == "__main__":
    main()
