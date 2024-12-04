
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def calculate_volatility(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y")
    volatility = hist['Close'].pct_change().std() * (252 ** 0.5)
    return volatility

def plot_three_portfolios_with_regression(portfolio_list, adjusted_portfolio_list, amount, close_prices_df):
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

    # Calculate regression lines
    date_numeric = (portfolio_value.index - portfolio_value.index.min()).days
    portfolio_coefficients = np.polyfit(date_numeric, portfolio_value, 1)
    portfolio_regression_line = np.polyval(portfolio_coefficients, date_numeric)

    adjusted_date_numeric = (adjusted_portfolio_value.index - adjusted_portfolio_value.index.min()).days
    adjusted_coefficients = np.polyfit(adjusted_date_numeric, adjusted_portfolio_value, 1)
    adjusted_regression_line = np.polyval(adjusted_coefficients, adjusted_date_numeric)

    # Get present day for the vertical line
    present_day = pd.Timestamp.now().normalize()

    # Create a date range up to 3 months into the future (no past extension)
    end_date = present_day + pd.Timedelta(days=90)
    extended_dates = pd.date_range(start=portfolio_value.index.min(), end=end_date)

    # Map the extended dates to numeric values for regression line projection
    extended_numeric = (extended_dates - portfolio_value.index.min()).days
    extended_portfolio_regression = np.polyval(portfolio_coefficients, extended_numeric)
    extended_adjusted_regression = np.polyval(adjusted_coefficients, extended_numeric)

    # 1. Projection for User's Portfolio
    plt.figure(figsize=(10, 6))
    plt.plot(portfolio_value.index, portfolio_value, label='Portfolio Value', color='blue')
    plt.plot(extended_dates, extended_portfolio_regression, label='Regression Line', color='red', linestyle='--')
    plt.axvline(x=present_day, color='black', linestyle=':', label='Present Day')
    plt.title('User Portfolio Projection with Regression')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value (USD)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('static/images/user_portfolio_projection.png')
    plt.close()

    # 2. Projection for Program's Suggested Portfolio
    plt.figure(figsize=(10, 6))
    plt.plot(adjusted_portfolio_value.index, adjusted_portfolio_value, label='Adjusted Portfolio Value', color='green')
    plt.plot(extended_dates, extended_adjusted_regression, label='Regression Line', color='orange', linestyle='--')
    plt.axvline(x=present_day, color='black', linestyle=':', label='Present Day')
    plt.title('Suggested Portfolio Projection with Regression')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value (USD)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('static/images/suggested_portfolio_projection.png')
    plt.close()

    # 3. Comparison of Both Regression Lines
    plt.figure(figsize=(10, 6))
    plt.plot(extended_dates, extended_portfolio_regression, label='User Portfolio Regression', color='red', linestyle='--')
    plt.plot(extended_dates, extended_adjusted_regression, label='Suggested Portfolio Regression', color='orange', linestyle='--')
    plt.axvline(x=present_day, color='black', linestyle=':', label='Present Day')
    plt.xlim(portfolio_value.index.min(), end_date)  # Match the first two graphs
    plt.title('Comparison of Regression Lines (Aligned with First Two Graphs)')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value (USD)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('static/images/comparison_regression_lines.png')
    plt.close()


def categorize_volatility(volatility):
    """Categorize volatility into user-friendly buckets."""
    if volatility <= 0.25:
        return "Low Volatility"
    elif volatility <= 0.5:
        return "Moderate Volatility"
    elif volatility <= 0.75:
        return "High Volatility"
    else:
        return "Extreme Volatility"

def create_tables_with_buckets(tickers):
    sp500_tickers = pd.read_csv('sp500_tickers_full_info.csv')

    current_table = pd.DataFrame(columns=['Ticker', 'Industry', 'Volatility'])
    suggested_table = pd.DataFrame(columns=['Suggested Ticker', 'Industry', 'Suggested Volatility'])

    for ticker in tickers:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Get the industry of the stock
        industry = info.get('industry', 'Unknown')
        
        # Calculate the volatility of the stock
        volatility = calculate_volatility(ticker)
        categorized_volatility = categorize_volatility(volatility)
        
        # Filter S&P 500 stocks in the same industry
        sp500_tickers_industry = sp500_tickers[sp500_tickers['industry'] == industry]
        
        # Calculate volatilities for all stocks in the same industry
        sp500_tickers_industry['volatility'] = sp500_tickers_industry['Ticker'].apply(calculate_volatility)
        
        # Find the stock with the lowest volatility
        min_volatility = sp500_tickers_industry.loc[sp500_tickers_industry['volatility'].idxmin()]
        suggested_volatility = min_volatility['volatility']
        categorized_suggested_volatility = categorize_volatility(suggested_volatility)
        
        # Append data to the respective tables
        current_table = current_table._append(
            {'Ticker': ticker, 'Industry': industry, 'Volatility': categorized_volatility},
            ignore_index=True
        )
        suggested_table = suggested_table._append(
            {'Suggested Ticker': min_volatility['Ticker'], 'Industry': industry, 'Suggested Volatility': categorized_suggested_volatility},
            ignore_index=True
        )

    return current_table, suggested_table


