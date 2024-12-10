import yfinance as yf
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
from volatility import calculate_volatility, plot_three_portfolios_with_regression, create_tables_with_buckets
import matplotlib
matplotlib.use('Agg')  # Use a backend that doesn't require a display
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

app = Flask(__name__)

# Function to validate the ticker
def is_valid_ticker(ticker):
    sp500 = pd.read_csv('CSVs/sp500_tickers_full_info.csv')
    # Convert all tickers in the CSV to uppercase
    sp500_tickers = [t.upper() for t in sp500['Ticker'].tolist()]
    
    # Check if the provided ticker (in uppercase) is in the S&P 500 ticker list
    return ticker.upper() in sp500_tickers

@app.route('/')
def index():
    tickers = request.args.getlist('tickers')
    prices = request.args.getlist('prices')
    error_message = request.args.get('error_message', '')

    # Combine tickers and prices into pairs for rendering
    ticker_price_pairs = list(zip(tickers, prices))

    return render_template(
        'index.html',
        ticker_price_pairs=ticker_price_pairs,
        error_message=error_message
    )

@app.route('/submit', methods=['POST'])
def submit():
    try:
        tickers_list = request.form.getlist('tickers')
        prices_list = request.form.getlist('prices')

        # Validate tickers: normalize to uppercase first
        tickers_list = [ticker.strip().upper() for ticker in tickers_list]
        valid_tickers = [ticker for ticker in tickers_list if is_valid_ticker(ticker)]
        invalid_tickers = [ticker for ticker in tickers_list if ticker not in valid_tickers]

        if invalid_tickers:
            error_message = f"The following tickers are invalid: {', '.join(invalid_tickers)}. Please correct them."
            return redirect(
                url_for(
                    'index',
                    tickers=tickers_list,
                    prices=prices_list,
                    error_message=error_message
                )
            )

        # Validate prices
        try:
            prices_list = [float(price.strip()) for price in prices_list]
        except ValueError:
            error_message = "Invalid price(s) entered. Ensure all prices are numeric values."
            return redirect(
                url_for(
                    'index',
                    tickers=tickers_list,
                    prices=prices_list,
                    error_message=error_message
                )
            )

        # Proceed with valid tickers and prices
        table1, table2 = create_tables_with_buckets(valid_tickers)
        all_closings = pd.read_csv('CSVs/closingPrices.csv')
        ticker_list = table1['Ticker'].tolist()
        suggested_ticker_list = table2['Suggested Ticker'].tolist()

        plot_three_portfolios_with_regression(ticker_list, suggested_ticker_list, prices_list, all_closings)

        # Render results
        return render_template(
            'results.html',
            table1=table1.to_html(classes='data-table', index=False),
            table2=table2.to_html(classes='data-table', index=False)
        )
    except Exception:
        return redirect(
            url_for(
                'index',
                error_message="An unexpected error occurred. Please try again."
            )
        )

if __name__ == '__main__':
    app.run(debug=True)
