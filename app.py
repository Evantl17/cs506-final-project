import yfinance as yf
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, jsonify
from volatility import calculate_volatility, plot_three_portfolios_with_regression, create_tables_with_buckets
import matplotlib
matplotlib.use('Agg')  # Use a backend that doesn't require a display
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from clustering import create_clusters, SimiliarCompany
from collections import defaultdict

app = Flask(__name__)

# Load full ticker info once at app start
sp500_info = pd.read_csv('CSVs/sp500_tickers_full_info.csv')
# Create a dictionary keyed by Ticker for quick lookups
sp500_info_dict = sp500_info.set_index('Ticker').to_dict(orient='index')
ticker_list = sp500_info['Ticker'].tolist()

@app.route('/get-tickers', methods=['GET'])
def get_tickers():
    return jsonify(ticker_list)  # Send the list as a JSON response

def is_valid_ticker(ticker):
    # Convert all tickers in the CSV to uppercase
    sp500_tickers = [t.upper() for t in sp500_info['Ticker'].tolist()]
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

        # Normalize and validate tickers
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

        # Perform your plotting
        plot_three_portfolios_with_regression(ticker_list, suggested_ticker_list, prices_list, all_closings)

        # Generate similar company recommendations
        similar_companies_dfs = []
        # Create clusters once
        cluster = create_clusters()
        
        for ticker in valid_tickers:
            # SimiliarCompany returns a list of similar tickers
            similar = SimiliarCompany(ticker, cluster)
            if similar:  # Only append if not empty
                similar_df = pd.DataFrame(similar, columns=['Similar Ticker'])
                similar_df['Base Ticker'] = ticker
                similar_companies_dfs.append(similar_df)

        if similar_companies_dfs:
            all_similar_companies = pd.concat(similar_companies_dfs, ignore_index=True)
        else:
            all_similar_companies = pd.DataFrame(columns=['Base Ticker', 'Similar Ticker'])

        # Convert to dictionary for easy iteration
        similar_comp_dict = defaultdict(list)
        for _, row in all_similar_companies.iterrows():
            similar_comp_dict[row['Base Ticker']].append(row['Similar Ticker'])

        # Enhance the dictionary with company name and price
        enhanced_sim_dict = {}
        for base_ticker, sims in similar_comp_dict.items():
            enhanced_list = []
            for sim_ticker in sims:
                info = sp500_info_dict.get(sim_ticker.upper())
                if info:
                    name = info.get('longName', sim_ticker)
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

        # Render results page with the enhanced similar companies dictionary
        return render_template(
            'results.html',
            table1=table1_html,
            table2=table2_html,
            similar_companies=enhanced_sim_dict
        )
    except Exception as e:
        print("Error:", e)
        return redirect(
            url_for(
                'index',
                error_message="An unexpected error occurred. Please try again."
            )
        )

if __name__ == '__main__':
    app.run(debug=True)
