
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

tickers = ['AAPL', 'GOOGL', 'AMZN', 'MSFT', 'TSLA']

def calculate_volatility(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")
    volatility = hist['Close'].pct_change().std() * (252 ** 0.5)
    return volatility

def plot_two_portfolios_with_regression(portfolio_list, adjusted_portfolio_list, amount, close_prices_df):
    # Ensure the 'Date' column is in datetime format and convert to UTC (or remove timezone)
    close_prices_df['Date'] = pd.to_datetime(close_prices_df['Date'], utc=True).dt.tz_convert(None)

    # Function to calculate the portfolio value
    def calculate_portfolio_value(ticker_list, amount, close_prices_df):
        portfolio_df = close_prices_df[close_prices_df['Ticker'].isin(ticker_list)].copy()
        pivot_df = portfolio_df.pivot(index='Date', columns='Ticker', values='Close')
        for i, ticker in enumerate(ticker_list):
            pivot_df[ticker] = pivot_df[ticker] / (pivot_df[ticker][pivot_df.index[-1]] / amount[i])
        portfolio_value = pivot_df.sum(axis=1)
        return portfolio_value

    # Calculate portfolio values for both portfolios
    portfolio_value = calculate_portfolio_value(portfolio_list, amount, close_prices_df)
    adjusted_portfolio_value = calculate_portfolio_value(adjusted_portfolio_list, amount, close_prices_df)

    # Plot the portfolio values
    plt.figure(figsize=(14, 7))
    plt.plot(portfolio_value.index, portfolio_value, label='Portfolio Value', color='blue')
    plt.plot(adjusted_portfolio_value.index, adjusted_portfolio_value, label='Adjusted Portfolio Value', color='green')

    # Add regression lines for both portfolios
    date_numeric = (portfolio_value.index - portfolio_value.index.min()).days
    coefficients = np.polyfit(date_numeric, portfolio_value, 1)
    regression_line = np.polyval(coefficients, date_numeric)
    plt.plot(portfolio_value.index, regression_line, label='Portfolio Regression Line', color='red', linestyle='--')

    adjusted_date_numeric = (adjusted_portfolio_value.index - adjusted_portfolio_value.index.min()).days
    adjusted_coefficients = np.polyfit(adjusted_date_numeric, adjusted_portfolio_value, 1)
    adjusted_regression_line = np.polyval(adjusted_coefficients, adjusted_date_numeric)
    plt.plot(adjusted_portfolio_value.index, adjusted_regression_line, label='Adjusted Portfolio Regression Line', color='orange', linestyle='--')

    # Add vertical line for present day
    present_day = pd.Timestamp.now().normalize()  # Get today's date without time
    plt.axvline(x=present_day, color='black', linestyle=':', label='Present Day')

    # Project future values for the next 3 months
    future_dates = pd.date_range(start=present_day, periods=90, freq='D')
    future_numeric = (future_dates - portfolio_value.index.min()).days

    # Calculate projected values
    projected_portfolio_values = np.polyval(coefficients, future_numeric)
    projected_adjusted_values = np.polyval(adjusted_coefficients, future_numeric)

    # Plot projections
    plt.plot(future_dates, projected_portfolio_values, label='Projected Portfolio Value', color='red', linestyle='--')
    plt.plot(future_dates, projected_adjusted_values, label='Projected Adjusted Portfolio Value', color='orange', linestyle='--')

    # Plot formatting
    plt.title('Portfolio Comparison Over Time')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value (USD)')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.savefig('static/images/portfolio_plot.png')
    plt.close()

def create_table(tickers):
    sp500_tickers = pd.read_csv('sp500_tickers_full_info.csv')

    table = pd.DataFrame()
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        industry = info['industry']
        
        volatility = calculate_volatility(ticker)
        
        sp500_tickers_industry = sp500_tickers[sp500_tickers['industry'] == industry]
        
        sp500_tickers_industry['volatility'] = sp500_tickers_industry['Ticker'].apply(calculate_volatility)
        
        min_volatility = sp500_tickers_industry.loc[sp500_tickers_industry['volatility'].idxmin()]
        
        
        table = table._append({'Ticker': ticker, 'Industry': industry, 'Volatility': volatility, "Suggested Ticker" : min_volatility['Ticker'], "Suggested Company Volatility" : min_volatility['volatility']}, ignore_index=True)
    return table


