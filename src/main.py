from fastapi import FastAPI
import pandas as pd
from extract import get_stock_price_today, get_stock_price_with_specific_date
from analysis import plot_price, plot_moving_average, plot_volume, plot_price_plotly
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
import plotly.express as px


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello" : "This is a stock api"}


@app.get("/today_price/{ticker}/{duration}")
def get_today(ticker: str, duration: int):
    
    data = get_stock_price_today(ticker, duration)

    return data.to_json()



@app.get("/get_price/{ticker}/{start_date}/{end_date}")
def get_today(ticker: str, start_date: str, end_date: str):
    
    data = get_stock_price_with_specific_date(ticker, start_date, end_date)

    return data.to_json()



@app.get("/plot_price/{ticker}/{duration}")
def plot_price_endpoint(ticker: str, duration: int):
    data = get_stock_price_today(ticker, duration)
    filename = "stockprices.png"
    plot_price(data, filename)
    return FileResponse(filename, media_type="image/png")
    
    
@app.get("/plot_moving_average/{ticker}/{duration}/{window}")
def plot_moving_average_endpoint(ticker: str, duration: int, window: int):
    data = get_stock_price_today(ticker, duration)
    filename = "moving_average.png"
    plot_moving_average(data, window, filename)
    return FileResponse(filename, media_type="image/png")



@app.get("/plot_volume/{ticker}/{duration}")
def plot_volume_endpoint(ticker: str, duration: int):
    data = get_stock_price_today(ticker, duration)
    filename = "volume.png"
    plot_volume(data, filename)
    return FileResponse(filename, media_type="image/png")



@app.get("/plot_price_plotly/{ticker}/{duration}")
def plot_price_plotly_endpoint(ticker: str, duration: int):
    data = get_stock_price_today(ticker, duration)
    fig = plot_price_plotly(data)
    return JSONResponse(content=fig.to_json())