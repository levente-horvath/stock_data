import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import riskfolio as rp
import pyfolio as pf
from extract import *
import mplfinance as mpf
import matplotlib.dates as mdates
import plotly.graph_objects as go


def plot_price(df, filename):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # Create a candlestick chart
    mpf.plot(df, type='candle', style='charles', title='Stock Price Over Time', ylabel='Price', savefig=filename)



def plot_price_plotly(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    fig = go.Figure(data=[go.Candlestick(x=df.index,
                                            open=df['Open'],
                                            high=df['High'],
                                            low=df['Low'],
                                            close=df['Close'])])

    fig.update_layout(title='Stock Price Over Time',
                        yaxis_title='Price')

    return fig

def plot_moving_average(df, window, filename):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df['Moving Average'] = df['Close'].rolling(window=window).mean()

    plt.figure(figsize=(12, 6))
    plt.plot(df['Close'], label='Close Price')
    plt.plot(df['Moving Average'], label=f'{window}-Day Moving Average')
    plt.title('Stock Price and Moving Average')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.savefig(filename)
    plt.close()

def plot_volume(df, filename):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    plt.figure(figsize=(12, 6))
    plt.bar(df.index, df['Volume'], color='blue')
    plt.title('Stock Volume Over Time')
    plt.xlabel('Date')
    plt.ylabel('Volume')
    plt.savefig(filename)
    plt.close()


def main():
    #data = get_stock_price_with_specific_date("ANET", "2024-3-1", "2025-3-6")
    data = get_stock_price_today("AMZN", 25)

    tr_data = transform_data(data)





if __name__ == "__main__":
    main()
