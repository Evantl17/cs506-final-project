import yfinance as yf
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

# Function to validate the ticker
def is_valid_ticker(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        # Check for the presence of a key that indicates a valid ticker
        return info and 'shortName' in info and info['shortName'] is not None
    except Exception as e:
        print(f"Error validating ticker {ticker}: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    tickers_list = request.form.getlist('tickers')
    prices_list = request.form.getlist('prices')

    # Validate the tickers and clean the data
    tickers_list = [ticker.strip().upper() for ticker in tickers_list]
    valid_tickers = [ticker for ticker in tickers_list if is_valid_ticker(ticker)]

    # Fetch stock data
    start_date = '2014-01-01'
    end_date = '2024-01-01'
    data = yf.download(valid_tickers, start=start_date, end=end_date)
    cleaned_data = data.dropna()

    # Prepare adjusted close price data for each ticker, limited to the last 20 values
    adj_close_data = cleaned_data['Adj Close']

    # Convert the data to HTML tables, limiting to the last 20 values
    tables = {}
    for ticker in valid_tickers:
        ticker_data = adj_close_data[[ticker]].dropna().tail(20)  # Get the last 20 values
        tables[ticker] = ticker_data.to_html(classes='data-table', border=0)

    return render_template('results.html', tables=tables, tickers_list=tickers_list, prices_list=prices_list)

if __name__ == '__main__':
    app.run(debug=True)
