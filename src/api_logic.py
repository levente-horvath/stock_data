from fastapi import FastAPI
import pandas as pd
from extract import get_stock_price_today, get_stock_price_with_specific_date
from transform import load_data, transform_data

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello" : "This is a stock api2"}


@app.get("/today_price/{ticker}/{duration}")
def get_today(ticker: str, duration: int):
    
    data = get_stock_price_today(ticker, duration)

    filename = "stockprices.csv"
    data.to_csv(filename)    
    # Ensure the file is saved before loading
    data.to_csv(filename, mode='w', index=True)
    
    # Load and transform the data
    loaded_data = load_data(filename)
    transformed_data = transform_data(loaded_data)[1]

    return transformed_data.to_json()



@app.get("/get_price/{ticker}/{start_date}/{end_date}")
def get_today(ticker: str, start_date: str, end_date: str):
    
    data = get_stock_price_with_specific_date(ticker, start_date, end_date)
    filename = "stockprices.csv"
    data.to_csv(filename)    
    # Ensure the file is saved before loading
    data.to_csv(filename, mode='w', index=True)
    
    # Load and transform the data
    loaded_data = load_data(filename)
    transformed_data = transform_data(loaded_data)[1]

    return transformed_data.to_json()






