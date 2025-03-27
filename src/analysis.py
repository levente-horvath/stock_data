import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import riskfolio as rp
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

def plot_moving_average_plotly(df, window):
    # Convert 'Date' column to datetime and set as index
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    
    # Calculate the moving average
    df['Moving Average'] = df['Close'].rolling(window=window).mean()

    # Convert data to plain lists to avoid base64 encoding in JSON
    x_values = df.index.strftime('%Y-%m-%d').tolist()  # Dates as strings
    y_close = df['Close'].tolist()                     # Closing prices as list
    y_moving_avg = df['Moving Average'].tolist()       # Moving averages as list

    # Create the Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_values, y=y_close, mode='lines', name='Close Price'))
    fig.add_trace(go.Scatter(x=x_values, y=y_moving_avg, mode='lines', name=f'{window}-Day Moving Average'))

    # Update layout with title and axis labels
    fig.update_layout(
        title='Stock Price and Moving Average',
        xaxis_title='Date',
        yaxis_title='Price'
    )

    return fig




def main():
    #data = get_stock_price_with_specific_date("ANET", "2024-3-1", "2025-3-6")
    data = get_stock_price_today("AMZN", 25)

    tr_data = transform_data(data)





if __name__ == "__main__":
    main()
