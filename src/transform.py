import pandas as pd
from utils import setup_logger
import sys
import json

logger = setup_logger(__name__)


def load_data(file_name="stockprices.csv"):
    try:
        df = pd.read_csv("stockprices.csv", sep=',', names=['Date', 'Close' , 'High' , 'Low' , 'Open', 'Volume'])
        return df
    except FileNotFoundError as fnf_error:
        logger.error(f"File not found: {fnf_error}")
        sys.exit(1)
    except Exception as err:
        logger.error(f"An error occurred: {err}")
        sys.exit(1)



def transform_data(data):

    #saving the name of the ticker
    ticker = data.iloc[1]
    ticker = ticker['Close']
    
    
    df = data.drop([0, 1, 2]).reset_index(drop=True)

    df['Date'] = pd.to_datetime(df['Date'])

    # Adding Moving averages to the data
    df['3D_MA'] = df['Close'].rolling(window=3).mean()
    df['5D_MA'] = df['Close'].rolling(window=5).mean()

    # Adding exponential moving averages
    df['3D_EMA'] = df['Close'].ewm(span=3, adjust=False).mean()
    df['5D_EMA'] = df['Close'].ewm(span=5, adjust=False).mean()

    return ticker, df





def main():
    data = load_data()
    ticker, tr_data = transform_data(data)

    filename = "transform_data.csv"
    
    tr_data.to_csv(filename)
    
    print(tr_data.info())

    logger.info(f"Transformed data has been saved to {filename}")
    
    metadata = [ticker]

    with open("data.meta.json", "w") as meta:
        json.dump(metadata, meta)

    logger.info("Metadata has been saved to data.meta.json")



if __name__ == "__main__":
    main()
