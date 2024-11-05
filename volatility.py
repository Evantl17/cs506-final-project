
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

def plot_two_portfolios_with_regression(portfolio_list, adjusted_portfolio_list, close_prices_df):
    # Ensure the 'Date' column is in datetime format and convert to UTC (or remove timezone)
    close_prices_df['Date'] = pd.to_datetime(close_prices_df['Date'], utc=True).dt.tz_convert(None)
    
    # Function to calculate the portfolio value
    def calculate_portfolio_value(ticker_list, close_prices_df):
        portfolio_df = close_prices_df[close_prices_df['Ticker'].isin(ticker_list)].copy()
        pivot_df = portfolio_df.pivot(index='Date', columns='Ticker', values='Close')
        portfolio_value = pivot_df.sum(axis=1)
        return portfolio_value

    # Calculate portfolio values for both portfolios
    portfolio_value = calculate_portfolio_value(portfolio_list, close_prices_df)
    adjusted_portfolio_value = calculate_portfolio_value(adjusted_portfolio_list, close_prices_df)

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

    # Plot formatting
    plt.title(f'Portfolio Comparison Over Time')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value (USD)')
    plt.grid(True)
    plt.legend()

    # Show the final value as text on the plot
    plt.text(portfolio_value.index[-1], portfolio_value.iloc[-1],
             f'Final Value: ${portfolio_value.iloc[-1]:.2f}', fontsize=12, color='blue')
    plt.text(adjusted_portfolio_value.index[-1], adjusted_portfolio_value.iloc[-1],
             f'Adjusted Final Value: ${adjusted_portfolio_value.iloc[-1]:.2f}', fontsize=12, color='green')

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


