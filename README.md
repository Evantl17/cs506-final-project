# cs506-final-project

Description of the project.

Our project takes the users investment portfolio, and displays a variety of data. This includes the calculated risk, overall portfolio ratings, individual stock ratings. Additonally, this project will give the user various recommendations on how to reduce risk, and maximize profit. Our target audience is entry-level investors who want to maximize returns while minimizing risk. It will provide the user complete oversight of their investments.

Clear goal(s) (e.g. Successfully predict the number of students attending lecture based on the weather report).

Succesfully predict future asset returns, compute accurate risk measurements. Create portfolio that minimizes risk. 

What data needs to be collected and how you will collect it (e.g. scraping xyz website or polling students).

We need historical stock market data which we will get from yfinance. We also need the users portfolio which will need to be inputed by the user.

How you plan on modeling the data (e.g. clustering, fitting a linear model, decision trees, XGBoost, some sort of deep learning method, etc.).

The data will be modeled via clustering. Clustering will be used to identify where the user's portfolio is high or low rish with the given rating. 

How do you plan on visualizing the data? (e.g. interactive t-SNE plot, scatter plot of feature x vs. feature y).

We are going to use the modern portfolio theory to make a scatter plot of volatility vs expected return. 

What is your test plan? (e.g. withhold 20% of data for testing, train on data collected in October and test on data collected in November, etc.).

We would withhold 20% for testing, and train the rest on data collected in the past decade of data. 
