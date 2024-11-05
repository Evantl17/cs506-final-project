import yfinance as yf
import numpy as np
import pandas as pd


ticker = 'AAPL'

sp500_tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol'].tolist()
print(sp500_tickers)

data = []

# Loop through each ticker and fetch all available information
for ticker in sp500_tickers:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info  # Get all available info as a dictionary
        info['Ticker'] = ticker  # Add the ticker symbol for reference
        data.append(info)
    except Exception as e:
        data.append({'Ticker': ticker, 'Error': 'Error fetching data'})

# Convert the data to a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv('sp500_tickers_full_info.csv', index=False)

print("CSV file 'sp500_tickers_full_info.csv' has been created.")





