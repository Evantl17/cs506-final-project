import yfinance as yf
import pandas as pd
from flask import Flask, render_template, request

# Set environment variable to skip loading .env file
import os
os.environ['FLASK_SKIP_DOTENV'] = '1'

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
    tickers = request.form['tickers']  
    tickers_list = tickers.split(",") 
    tickers_list = [ticker.strip().upper() for ticker in tickers_list] 
    print(tickers_list)
    start_date = '2014-01-01' 
    end_date = '2024-01-01'   

    # Validate the tickers
    valid_tickers = [ticker for ticker in tickers_list if is_valid_ticker(ticker)]
    data = yf.download(valid_tickers, start=start_date, end=end_date)

    cleaned_data = data.dropna()

    adj_close_data = cleaned_data['Adj Close']
    return f"{adj_close_data.isna().sum()}"

if __name__ == '__main__':
    app.run(debug=True)
