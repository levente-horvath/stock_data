from fastapi import FastAPI
import pandas as pd
from extract import get_stock_price_today, get_stock_price_with_specific_date
from analysis import plot_price, plot_moving_average, plot_volume, plot_price_plotly, plot_moving_average_plotly, plot_macd, plot_macd_plotly, plot_obv, plot_obv_plotly, plot_vwap, plot_vwap_plotly, plot_adl, plot_adl_plotly, plot_ichimoku, plot_ichimoku_plotly, plot_stochastic, plot_stochastic_plotly, plot_cci, plot_cci_plotly, plot_parabolic_sar, plot_parabolic_sar_plotly, plot_std_dev, plot_std_dev_plotly, plot_atr, plot_atr_plotly, plot_ad_line, plot_ad_line_plotly
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


@app.get("/plot_volume_plotly/{ticker}/{duration}")
def plot_volume_plotly_endpoint(ticker: str, duration: int):
    data = get_stock_price_today(ticker, duration)
    fig = px.bar(data, x=data.index, y="Volume", title=f"Volume for {ticker}")
    return JSONResponse(content=fig.to_json())


@app.get("/plot_price_plotly/{ticker}/{duration}")
def plot_price_plotly_endpoint(ticker: str, duration: int):
    data = get_stock_price_today(ticker, duration)
    fig = plot_price_plotly(data)
    return JSONResponse(content=fig.to_json())


@app.get("/plot_moving_average_plotly/{ticker}/{duration}/{window}")
def plot_moving_average_plotly_endpoint(ticker: str, duration: int, window: int):
    data = get_stock_price_today(ticker, duration)
    fig = plot_moving_average_plotly(data, window)
    return JSONResponse(content=fig.to_json())


@app.get("/plot_macd/{ticker}/{duration}")
def plot_macd_endpoint(ticker: str, duration: int):
    data = get_stock_price_today(ticker, duration)
    filename = "macd.png"
    plot_macd(data, filename)
    return FileResponse(filename, media_type="image/png")


@app.get("/plot_macd_plotly/{ticker}/{duration}")
def plot_macd_plotly_endpoint(ticker: str, duration: int):
    data = get_stock_price_today(ticker, duration)
    fig = plot_macd_plotly(data)
    return JSONResponse(content=fig.to_json())


@app.get("/plot_obv/{ticker}/{duration}")
def plot_obv_endpoint(ticker: str, duration: int):
    data = get_stock_price_today(ticker, duration)
    filename = "obv.png"
    plot_obv(data, filename)
    return FileResponse(filename, media_type="image/png")


@app.get("/plot_obv_plotly/{ticker}/{duration}")
def plot_obv_plotly_endpoint(ticker: str, duration: int):
    data = get_stock_price_today(ticker, duration)
    fig = plot_obv_plotly(data)
    return JSONResponse(content=fig.to_json())


@app.get("/plot_vwap/{ticker}/{duration}")
def plot_vwap_endpoint(ticker: str, duration: int):
    data = get_stock_price_today(ticker, duration)
    filename = "vwap.png"
    plot_vwap(data, filename)
    return FileResponse(filename, media_type="image/png")


@app.get("/plot_vwap_plotly/{ticker}/{duration}")
def plot_vwap_plotly_endpoint(ticker: str, duration: int):
    data = get_stock_price_today(ticker, duration)
    fig = plot_vwap_plotly(data)
    return JSONResponse(content=fig.to_json())


@app.get("/plot_adl/{ticker}/{duration}")
def plot_adl_endpoint(ticker: str, duration: int):
    data = get_stock_price_today(ticker, duration)
    filename = "adl.png"
    plot_adl(data, filename)
    return FileResponse(filename, media_type="image/png")


@app.get("/plot_adl_plotly/{ticker}/{duration}")
def plot_adl_plotly_endpoint(ticker: str, duration: int):
    data = get_stock_price_today(ticker, duration)
    fig = plot_adl_plotly(data)
    return JSONResponse(content=fig.to_json())


@app.get("/plot_ichimoku/{ticker}/{duration}")
def plot_ichimoku_endpoint(ticker: str, duration: int):
    data = get_stock_price_today(ticker, duration)
    filename = "ichimoku.png"
    plot_ichimoku(data, filename)
    return FileResponse(filename, media_type="image/png")


@app.get("/plot_ichimoku_plotly/{ticker}/{duration}")
def plot_ichimoku_plotly_endpoint(ticker: str, duration: int):
    data = get_stock_price_today(ticker, duration)
    fig = plot_ichimoku_plotly(data)
    return JSONResponse(content=fig.to_json())


@app.get("/plot_stochastic/{ticker}/{duration}")
def plot_stochastic_endpoint(ticker: str, duration: int):
    data = get_stock_price_today(ticker, duration)
    filename = "stochastic.png"
    plot_stochastic(data, filename)
    return FileResponse(filename, media_type="image/png")


@app.get("/plot_stochastic_plotly/{ticker}/{duration}")
def plot_stochastic_plotly_endpoint(ticker: str, duration: int):
    data = get_stock_price_today(ticker, duration)
    fig = plot_stochastic_plotly(data)
    return JSONResponse(content=fig.to_json())


@app.get("/plot_cci/{ticker}/{duration}")
def plot_cci_endpoint(ticker: str, duration: int):
    data = get_stock_price_today(ticker, duration)
    filename = "cci.png"
    plot_cci(data, filename)
    return FileResponse(filename, media_type="image/png")


@app.get("/plot_cci_plotly/{ticker}/{duration}")
def plot_cci_plotly_endpoint(ticker: str, duration: int):
    data = get_stock_price_today(ticker, duration)
    fig = plot_cci_plotly(data)
    return JSONResponse(content=fig.to_json())


@app.get("/plot_parabolic_sar/{ticker}/{duration}")
def plot_parabolic_sar_endpoint(ticker: str, duration: int):
    data = get_stock_price_today(ticker, duration)
    filename = "parabolic_sar.png"
    plot_parabolic_sar(data, filename)
    return FileResponse(filename, media_type="image/png")


@app.get("/plot_parabolic_sar_plotly/{ticker}/{duration}")
def plot_parabolic_sar_plotly_endpoint(ticker: str, duration: int):
    data = get_stock_price_today(ticker, duration)
    fig = plot_parabolic_sar_plotly(data)
    return JSONResponse(content=fig.to_json())


@app.get("/plot_std_dev/{ticker}/{duration}")
def plot_std_dev_endpoint(ticker: str, duration: int):
    data = get_stock_price_today(ticker, duration)
    filename = "std_dev.png"
    plot_std_dev(data, filename)
    return FileResponse(filename, media_type="image/png")


@app.get("/plot_std_dev_plotly/{ticker}/{duration}")
def plot_std_dev_plotly_endpoint(ticker: str, duration: int):
    data = get_stock_price_today(ticker, duration)
    fig = plot_std_dev_plotly(data)
    return JSONResponse(content=fig.to_json())


@app.get("/plot_atr/{ticker}/{duration}")
def plot_atr_endpoint(ticker: str, duration: int):
    data = get_stock_price_today(ticker, duration)
    filename = "atr.png"
    plot_atr(data, filename)
    return FileResponse(filename, media_type="image/png")


@app.get("/plot_atr_plotly/{ticker}/{duration}")
def plot_atr_plotly_endpoint(ticker: str, duration: int):
    data = get_stock_price_today(ticker, duration)
    fig = plot_atr_plotly(data)
    return JSONResponse(content=fig.to_json())


@app.get("/plot_ad_line/{ticker}/{duration}")
def plot_ad_line_endpoint(ticker: str, duration: int):
    data = get_stock_price_today(ticker, duration)
    filename = "ad_line.png"
    plot_ad_line(data, filename)
    return FileResponse(filename, media_type="image/png")


@app.get("/plot_ad_line_plotly/{ticker}/{duration}")
def plot_ad_line_plotly_endpoint(ticker: str, duration: int):
    data = get_stock_price_today(ticker, duration)
    fig = plot_ad_line_plotly(data)
    return JSONResponse(content=fig.to_json())