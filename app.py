import yfinance as yf
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from volatility import calculate_volatility, plot_three_portfolios_with_regression, create_tables_with_buckets
import matplotlib
matplotlib.use('Agg')  # Use a backend that doesn't require a display
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from clustering import create_clusters, SimiliarCompany
from collections import defaultdict
import os

app = Flask(__name__)
app.secret_key = "thomasssss"  # Set a secret key for session management

# Load full ticker info once at app start
sp500_info = pd.read_csv('CSVs/sp500_tickers_full_info.csv')
sp500_info_dict = sp500_info.set_index('Ticker').to_dict(orient='index')
all_closings = pd.read_csv('CSVs/closingPrices.csv')  # load once
ticker_list = sp500_info['Ticker'].tolist()

@app.route('/get-tickers', methods=['GET'])
def get_tickers():
    return jsonify(ticker_list)  # Send the list as a JSON response

def is_valid_ticker(ticker):
    sp500_tickers = [t.upper() for t in sp500_info['Ticker'].tolist()]
    return ticker.upper() in sp500_tickers

def generate_results(valid_tickers, prices_list, suggested_tickers=None):
    table1, table2 = create_tables_with_buckets(valid_tickers)

    # If we have saved suggested_tickers, override the suggested ticker column in table2
    if suggested_tickers is not None and 'Suggested Ticker' in table2.columns:
        if len(suggested_tickers) == len(table2):
            table2['Suggested Ticker'] = suggested_tickers
    else:
        suggested_tickers = table2['Suggested Ticker'].tolist()

    # Perform plotting
    user_ticker_list = table1['Ticker'].tolist()
    suggested_ticker_list = table2['Suggested Ticker'].tolist()

    plot_three_portfolios_with_regression(user_ticker_list, suggested_ticker_list, prices_list, all_closings)

    # Generate similar companies recommendations
    cluster = create_clusters()
    similar_companies_dfs = []
    for ticker in valid_tickers:
        similar = SimiliarCompany(ticker, cluster)
        if similar:  
            similar_df = pd.DataFrame(similar, columns=['Similar Ticker'])
            similar_df['Base Ticker'] = ticker
            similar_companies_dfs.append(similar_df)

    if similar_companies_dfs:
        all_similar_companies = pd.concat(similar_companies_dfs, ignore_index=True)
    else:
        all_similar_companies = pd.DataFrame(columns=['Base Ticker', 'Similar Ticker'])

    # Convert to dictionary
    similar_comp_dict = defaultdict(list)
    for _, row in all_similar_companies.iterrows():
        similar_comp_dict[row['Base Ticker']].append(row['Similar Ticker'])

    # Enhance with company name and price
    enhanced_sim_dict = {}
    for base_ticker, sims in similar_comp_dict.items():
        enhanced_list = []
        for sim_ticker in sims:
            info = sp500_info_dict.get(sim_ticker.upper())
            if info:
                name = info.get('shortName', sim_ticker)
                price = info.get('currentPrice', 'N/A')
                enhanced_list.append({
                    'ticker': sim_ticker,
                    'name': name,
                    'price': price
                })
        if enhanced_list:
            enhanced_sim_dict[base_ticker] = enhanced_list

    # Convert DataFrames to HTML
    table1_html = table1.to_html(classes='data-table', index=False)
    table2_html = table2.to_html(classes='data-table', index=False)

    # Save state in session
    session['valid_tickers'] = valid_tickers
    session['prices_list'] = prices_list
    session['suggested_tickers'] = suggested_tickers

    return render_template(
        'results.html',
        table1=table1_html,
        table2=table2_html,
        similar_companies=enhanced_sim_dict,
        user_ticker_list=user_ticker_list
    )

@app.route('/')
def index():
    tickers = request.args.getlist('tickers')
    prices = request.args.getlist('prices')
    error_message = request.args.get('error_message', '')

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

        tickers_list = [ticker.strip().upper() for ticker in tickers_list]
        valid_tickers = [t for t in tickers_list if is_valid_ticker(t)]
        invalid_tickers = [t for t in tickers_list if t not in valid_tickers]
        
        invalid_prices = [p for p in prices_list if int(p) < 0]
                
        if invalid_prices:
            error_message = f"The following prices are invalid: {', '.join(invalid_prices)}. Please correct them."
            return redirect(url_for('index', tickers=tickers_list, prices=prices_list, error_message=error_message))

        if invalid_tickers:
            error_message = f"The following tickers are invalid: {', '.join(invalid_tickers)}. Please correct them."
            return redirect(url_for('index', tickers=tickers_list, prices=prices_list, error_message=error_message))

        try:
            prices_list = [float(price.strip()) for price in prices_list]
        except ValueError:
            error_message = "Invalid price(s) entered. Ensure all prices are numeric values."
            return redirect(url_for('index', tickers=tickers_list, prices=prices_list, error_message=error_message))

        return generate_results(valid_tickers, prices_list)

    except Exception as e:
        print("Error:", e)
        return redirect(url_for('index', error_message="An unexpected error occurred. Please try again."))

@app.route('/bulk_replace', methods=['POST'])
def bulk_replace():
    valid_tickers = session.get('valid_tickers', [])
    prices_list = session.get('prices_list', [])
    suggested_tickers = session.get('suggested_tickers', [])

    table1, table2 = create_tables_with_buckets(valid_tickers)
    user_ticker_list = table1['Ticker'].tolist()

    # For each base ticker, check if a new replacement was chosen
    for i, base_ticker in enumerate(user_ticker_list):
        field_name = f"replacement_{base_ticker}"
        new_ticker = request.form.get(field_name, "").strip()
        if new_ticker:
            suggested_tickers[i] = new_ticker.upper()

    return generate_results(valid_tickers, prices_list, suggested_tickers=suggested_tickers)

if __name__ == '__main__':
    app.run(debug=True)
