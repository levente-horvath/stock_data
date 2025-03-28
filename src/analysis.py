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


def plot_macd(df, filename):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # Calculate MACD and Signal Line
    short_ema = df['Close'].ewm(span=12, adjust=False).mean()  # 12-day EMA
    long_ema = df['Close'].ewm(span=26, adjust=False).mean()   # 26-day EMA
    df['MACD'] = short_ema - long_ema                         # MACD Line
    df['Signal Line'] = df['MACD'].ewm(span=9, adjust=False).mean()  # Signal Line

    # Plot MACD and Signal Line
    plt.figure(figsize=(12, 6))
    plt.plot(df['MACD'], label='MACD', color='blue')
    plt.plot(df['Signal Line'], label='Signal Line', color='red')
    plt.title('MACD (Moving Average Convergence Divergence)')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend()
    plt.savefig(filename)
    plt.close()


def plot_macd_plotly(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # Calculate MACD and Signal Line
    short_ema = df['Close'].ewm(span=12, adjust=False).mean()  # 12-day EMA
    long_ema = df['Close'].ewm(span=26, adjust=False).mean()   # 26-day EMA
    df['MACD'] = short_ema - long_ema                         # MACD Line
    df['Signal Line'] = df['MACD'].ewm(span=9, adjust=False).mean()  # Signal Line

    # Create the Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], mode='lines', name='MACD', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df.index, y=df['Signal Line'], mode='lines', name='Signal Line', line=dict(color='red')))

    # Update layout with title and axis labels
    fig.update_layout(
        title='MACD (Moving Average Convergence Divergence)',
        xaxis_title='Date',
        yaxis_title='Value'
    )

    return fig

def plot_obv(df, filename):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # Calculate On-Balance Volume (OBV)
    df['OBV'] = (np.sign(df['Close'].diff()) * df['Volume']).fillna(0).cumsum()

    # Plot OBV
    plt.figure(figsize=(12, 6))
    plt.plot(df['OBV'], label='On-Balance Volume', color='purple')
    plt.title('On-Balance Volume (OBV)')
    plt.xlabel('Date')
    plt.ylabel('OBV')
    plt.legend()
    plt.savefig(filename)
    plt.close()


def plot_obv_plotly(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # Calculate On-Balance Volume (OBV)
    df['OBV'] = (np.sign(df['Close'].diff()) * df['Volume']).fillna(0).cumsum()

    # Create the Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['OBV'], mode='lines', name='OBV', line=dict(color='purple')))

    # Update layout with title and axis labels
    fig.update_layout(
        title='On-Balance Volume (OBV)',
        xaxis_title='Date',
        yaxis_title='OBV'
    )

    return fig

def plot_vwap(df, filename):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # Calculate VWAP
    df['VWAP'] = (df['Close'] * df['Volume']).cumsum() / df['Volume'].cumsum()

    # Plot VWAP
    plt.figure(figsize=(12, 6))
    plt.plot(df['Close'], label='Close Price')
    plt.plot(df['VWAP'], label='VWAP', color='orange')
    plt.title('Volume Weighted Average Price (VWAP)')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.savefig(filename)
    plt.close()

def plot_vwap_plotly(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # Calculate VWAP
    df['VWAP'] = (df['Close'] * df['Volume']).cumsum() / df['Volume'].cumsum()

    # Create the Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close Price'))
    fig.add_trace(go.Scatter(x=df.index, y=df['VWAP'], mode='lines', name='VWAP', line=dict(color='orange')))

    # Update layout with title and axis labels
    fig.update_layout(
        title='Volume Weighted Average Price (VWAP)',
        xaxis_title='Date',
        yaxis_title='Price'
    )

    return fig

def plot_adl(df, filename):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # Calculate ADL
    df['Money Flow Multiplier'] = ((df['Close'] - df['Low']) - (df['High'] - df['Close'])) / (df['High'] - df['Low'])
    df['Money Flow Volume'] = df['Money Flow Multiplier'] * df['Volume']
    df['ADL'] = df['Money Flow Volume'].cumsum()

    # Plot ADL
    plt.figure(figsize=(12, 6))
    plt.plot(df['ADL'], label='Accumulation/Distribution Line', color='green')
    plt.title('Accumulation/Distribution Line (ADL)')
    plt.xlabel('Date')
    plt.ylabel('ADL')
    plt.legend()
    plt.savefig(filename)
    plt.close()

def plot_adl_plotly(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # Calculate ADL
    df['Money Flow Multiplier'] = ((df['Close'] - df['Low']) - (df['High'] - df['Close'])) / (df['High'] - df['Low'])
    df['Money Flow Volume'] = df['Money Flow Multiplier'] * df['Volume']
    df['ADL'] = df['Money Flow Volume'].cumsum()

    # Create the Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['ADL'], mode='lines', name='ADL', line=dict(color='green')))

    # Update layout with title and axis labels
    fig.update_layout(
        title='Accumulation/Distribution Line (ADL)',
        xaxis_title='Date',
        yaxis_title='ADL'
    )

    return fig

def plot_ichimoku(df, filename):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # Calculate Ichimoku components
    df['Tenkan-sen'] = (df['High'].rolling(window=9).max() + df['Low'].rolling(window=9).min()) / 2
    df['Kijun-sen'] = (df['High'].rolling(window=26).max() + df['Low'].rolling(window=26).min()) / 2
    df['Senkou Span A'] = ((df['Tenkan-sen'] + df['Kijun-sen']) / 2).shift(26)
    df['Senkou Span B'] = ((df['High'].rolling(window=52).max() + df['Low'].rolling(window=52).min()) / 2).shift(26)

    # Plot Ichimoku Cloud
    plt.figure(figsize=(12, 6))
    plt.plot(df['Close'], label='Close Price')
    plt.plot(df['Tenkan-sen'], label='Tenkan-sen', color='red')
    plt.plot(df['Kijun-sen'], label='Kijun-sen', color='blue')
    plt.fill_between(df.index, df['Senkou Span A'], df['Senkou Span B'], color='gray', alpha=0.3, label='Ichimoku Cloud')
    plt.title('Ichimoku Cloud')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.savefig(filename)
    plt.close()

def plot_ichimoku_plotly(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # Calculate Ichimoku components
    df['Tenkan-sen'] = (df['High'].rolling(window=9).max() + df['Low'].rolling(window=9).min()) / 2
    df['Kijun-sen'] = (df['High'].rolling(window=26).max() + df['Low'].rolling(window=26).min()) / 2
    df['Senkou Span A'] = ((df['Tenkan-sen'] + df['Kijun-sen']) / 2).shift(26)
    df['Senkou Span B'] = ((df['High'].rolling(window=52).max() + df['Low'].rolling(window=52).min()) / 2).shift(26)

    # Create the Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close Price'))
    fig.add_trace(go.Scatter(x=df.index, y=df['Tenkan-sen'], mode='lines', name='Tenkan-sen', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=df.index, y=df['Kijun-sen'], mode='lines', name='Kijun-sen', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df.index, y=df['Senkou Span A'], mode='lines', name='Senkou Span A', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=df.index, y=df['Senkou Span B'], mode='lines', name='Senkou Span B', line=dict(color='orange')))
    fig.update_layout(
        title='Ichimoku Cloud',
        xaxis_title='Date',
        yaxis_title='Price'
    )

    return fig

def plot_stochastic(df, filename):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # Calculate Stochastic Oscillator
    df['%K'] = ((df['Close'] - df['Low'].rolling(window=14).min()) / 
                (df['High'].rolling(window=14).max() - df['Low'].rolling(window=14).min())) * 100
    df['%D'] = df['%K'].rolling(window=3).mean()

    # Plot Stochastic Oscillator
    plt.figure(figsize=(12, 6))
    plt.plot(df['%K'], label='%K', color='blue')
    plt.plot(df['%D'], label='%D', color='red')
    plt.title('Stochastic Oscillator')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend()
    plt.savefig(filename)
    plt.close()

def plot_stochastic_plotly(df):
    df['Date'] = pd.to_datetime(df['De'])
    df.set_index('Date', inplace=True)

    # Calculate Stochastic Oscillator
    df['%K'] = ((df['Close'] - df['Low'].rolling(window=14).min()) / 
                (df['High'].rolling(window=14).max() - df['Low'].rolling(window=14).min())) * 100
    df['%D'] = df['%K'].rolling(window=3).mean()

    # Create the Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['%K'], mode='lines', name='%K', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df.index, y=df['%D'], mode='lines', name='%D', line=dict(color='red')))
    fig.update_layout(
        title='Stochastic Oscillator',
        xaxis_title='Date',
        yaxis_title='Value'
    )

    return fig

def plot_cci(df, filename):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # Calculate CCI
    df['TP'] = (df['High'] + df['Low'] + df['Close']) / 3
    df['CCI'] = (df['TP'] - df['TP'].rolling(window=20).mean()) / (0.015 * df['TP'].rolling(window=20).std())

    # Plot CCI
    plt.figure(figsize=(12, 6))
    plt.plot(df['CCI'], label='CCI', color='blue')
    plt.axhline(100, color='red', linestyle='--', label='Overbought')
    plt.axhline(-100, color='green', linestyle='--', label='Oversold')
    plt.title('Commodity Channel Index (CCI)')
    plt.xlabel('Date')
    plt.ylabel('CCI')
    plt.legend()
    plt.savefig(filename)
    plt.close()

def plot_cci_plotly(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # Calculate CCI
    df['TP'] = (df['High'] + df['Low'] + df['Close']) / 3
    df['CCI'] = (df['TP'] - df['TP'].rolling(window=20).mean()) / (0.015 * df['TP'].rolling(window=20).std())

    # Create the Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['CCI'], mode='lines', name='CCI', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df.index, y=[100] * len(df), mode='lines', name='Overbought', line=dict(color='red', dash='dash')))
    fig.add_trace(go.Scatter(x=df.index, y=[-100] * len(df), mode='lines', name='Oversold', line=dict(color='green', dash='dash')))
    fig.update_layout(
        title='Commodity Channel Index (CCI)',
        xaxis_title='Date',
        yaxis_title='CCI'
    )

    return fig

def plot_parabolic_sar(df, filename):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # Calculate Parabolic SAR manually
    df['SAR'] = np.nan
    af = 0.02  # Acceleration factor
    max_af = 0.2
    trend = 1  # 1 for uptrend, -1 for downtrend
    ep = df['Low'][0] if trend == 1 else df['High'][0]  # Extreme point
    sar = df['High'][0] if trend == 1 else df['Low'][0]  # Initial SAR

    for i in range(1, len(df)):
        prev_sar = sar
        sar = prev_sar + af * (ep - prev_sar)

        if trend == 1:  # Uptrend
            if df['Low'][i] < sar:
                trend = -1
                sar = ep
                ep = df['High'][i]
                af = 0.02
            else:
                if df['High'][i] > ep:
                    ep = df['High'][i]
                    af = min(af + 0.02, max_af)
        else:  # Downtrend
            if df['High'][i] > sar:
                trend = 1
                sar = ep
                ep = df['Low'][i]
                af = 0.02
            else:
                if df['Low'][i] < ep:
                    ep = df['Low'][i]
                    af = min(af + 0.02, max_af)

        df.loc[df.index[i], 'SAR'] = sar

    # Plot Parabolic SAR
    plt.figure(figsize=(12, 6))
    plt.plot(df['Close'], label='Close Price', color='blue')
    plt.scatter(df.index, df['SAR'], label='Parabolic SAR', color='red', s=10)
    plt.title('Parabolic SAR')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.savefig(filename)
    plt.close()

def plot_parabolic_sar_plotly(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # Calculate Parabolic SAR manually (same logic as above)
    df['SAR'] = np.nan
    af = 0.02
    max_af = 0.2
    trend = 1
    ep = df['Low'][0] if trend == 1 else df['High'][0]
    sar = df['High'][0] if trend == 1 else df['Low'][0]

    for i in range(1, len(df)):
        prev_sar = sar
        sar = prev_sar + af * (ep - prev_sar)

        if trend == 1:
            if df['Low'][i] < sar:
                trend = -1
                sar = ep
                ep = df['High'][i]
                af = 0.02
            else:
                if df['High'][i] > ep:
                    ep = df['High'][i]
                    af = min(af + 0.02, max_af)
        else:
            if df['High'][i] > sar:
                trend = 1
                sar = ep
                ep = df['Low'][i]
                af = 0.02
            else:
                if df['Low'][i] < ep:
                    ep = df['Low'][i]
                    af = min(af + 0.02, max_af)

        df.loc[df.index[i], 'SAR'] = sar

    # Create the Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close Price', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df.index, y=df['SAR'], mode='markers', name='Parabolic SAR', marker=dict(color='red', size=5)))
    fig.update_layout(
        title='Parabolic SAR',
        xaxis_title='Date',
        yaxis_title='Price'
    )

    return fig

def plot_std_dev(df, filename):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # Calculate Standard Deviation
    df['Std Dev'] = df['Close'].rolling(window=20).std()

    # Plot Standard Deviation
    plt.figure(figsize=(12, 6))
    plt.plot(df['Std Dev'], label='Standard Deviation', color='blue')
    plt.title('Standard Deviation of Closing Prices')
    plt.xlabel('Date')
    plt.ylabel('Standard Deviation')
    plt.legend()
    plt.savefig(filename)
    plt.close()

def plot_std_dev_plotly(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # Calculate Standard Deviation
    df['Std Dev'] = df['Close'].rolling(window=20).std()

    # Create the Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Std Dev'], mode='lines', name='Standard Deviation', line=dict(color='blue')))
    fig.update_layout(
        title='Standard Deviation of Closing Prices',
        xaxis_title='Date',
        yaxis_title='Standard Deviation'
    )

    return fig

def plot_atr(df, filename):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # Calculate ATR manually
    df['TR'] = np.maximum(df['High'] - df['Low'], 
                          np.maximum(abs(df['High'] - df['Close'].shift(1)), 
                                     abs(df['Low'] - df['Close'].shift(1))))
    df['ATR'] = df['TR'].rolling(window=14).mean()

    # Plot ATR
    plt.figure(figsize=(12, 6))
    plt.plot(df['ATR'], label='Average True Range (ATR)', color='blue')
    plt.title('Average True Range (ATR)')
    plt.xlabel('Date')
    plt.ylabel('ATR')
    plt.legend()
    plt.savefig(filename)
    plt.close()

def plot_atr_plotly(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # Calculate ATR manually (same logic as above)
    df['TR'] = np.maximum(df['High'] - df['Low'], 
                          np.maximum(abs(df['High'] - df['Close'].shift(1)), 
                                     abs(df['Low'] - df['Close'].shift(1))))
    df['ATR'] = df['TR'].rolling(window=14).mean()

    # Create the Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['ATR'], mode='lines', name='ATR', line=dict(color='blue')))
    fig.update_layout(
        title='Average True Range (ATR)',
        xaxis_title='Date',
        yaxis_title='ATR'
    )

    return fig

def plot_ad_line(df, filename):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # Calculate A/D Line
    df['Money Flow Multiplier'] = ((df['Close'] - df['Low']) - (df['High'] - df['Close'])) / (df['High'] - df['Low'])
    df['Money Flow Volume'] = df['Money Flow Multiplier'] * df['Volume']
    df['AD Line'] = df['Money Flow Volume'].cumsum()

    # Plot A/D Line
    plt.figure(figsize=(12, 6))
    plt.plot(df['AD Line'], label='Accumulation/Distribution Line', color='green')
    plt.title('Accumulation/Distribution Line (A/D Line)')
    plt.xlabel('Date')
    plt.ylabel('A/D Line')
    plt.legend()
    plt.savefig(filename)
    plt.close()

def plot_ad_line_plotly(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # Calculate A/D Line
    df['Money Flow Multiplier'] = ((df['Close'] - df['Low']) - (df['High'] - df['Close'])) / (df['High'] - df['Low'])
    df['Money Flow Volume'] = df['Money Flow Multiplier'] * df['Volume']
    df['AD Line'] = df['Money Flow Volume'].cumsum()

    # Create the Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['AD Line'], mode='lines', name='A/D Line', line=dict(color='green')))
    fig.update_layout(
        title='Accumulation/Distribution Line (A/D Line)',
        xaxis_title='Date',
        yaxis_title='A/D Line'
    )

    return fig

def main():
    #data = get_stock_price_with_specific_date("ANET", "2024-3-1", "2025-3-6")
    data = get_stock_price_today("AMZN", 25)

    tr_data = transform_data(data)





if __name__ == "__main__":
    main()
