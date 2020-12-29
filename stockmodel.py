import streamlit as st
import pandas as pd 
import yfinance as yf 
import csv

## sudo code ##
    # 1. gather list of tickers and display as a filter (Complete)
    # 2. set other parameters (amount to buy, % of trade offs, etc.) (Complete)
    # 3. show reccomendation for today's purchase
    # 4. show graph of backtesting

filename = 'nasdaq_screener_1609165990883.csv'

df = pd.read_csv(filename)

stocks = st.sidebar.selectbox('Select Your Investment:',df['Symbol'].tolist())
time_period = st.sidebar.slider('Maximum Historical Look Back (Months):',min_value=1, max_value=24)
ten_percent = st.sidebar.number_input('Amount to invest if stock is 0 - 10 percent below the high:')
twenty_percent = st.sidebar.number_input('Amount to invest if stock is 10 - 20 percent below the high:')
thirty_percent = st.sidebar.number_input('Amount to invest if stock is 20 - 30 percent below the high:')

run = st.sidebar.button("Run")

if run:
    stock = yf.Ticker(stocks)
    lookback = str(time_period) + 'mo'
    hist = stock.history(period=lookback)
    high = max(hist['High'])
    current = (hist.tail(1)['Close'].iloc[0])
    percent_from_high = (1-(current/high))*100
    st.write(f"The high for the last {time_period} month(s) is ${round(high,2)}. The current price is ${round(current,2)} which is {round(percent_from_high,2)}% off the high.")
    
    if percent_from_high <= 10:
        suggestion = ten_percent
    elif percent_from_high > 10 and percent_from_high <= 20:
        suggestion = twenty_percent
    else:
        suggestion = thirty_percent

    st.write(f"Investment Reccomendation: ${round(suggestion,2)} in {stocks}.")
    st.line_chart(hist.drop(['Volume', 'Stock Splits', 'Dividends','Close','Open','Low'], axis=1))
    st.success('Success!')
else:
    st.title("Welcome!")
    st.write("Choose a stock to analyze on the left.")
    dj = yf.Ticker('^DJI')
    hist = dj.history(period ='max')
    st.line_chart(hist.drop(['Volume', 'Stock Splits', 'Dividends','Close','Open','Low'], axis=1))