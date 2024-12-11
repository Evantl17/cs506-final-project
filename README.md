# CS506 Final Project - Portfolio Analysis

## How to Build and Run
```
make install  # Install dependencies
make run     # Run analysis
make test    # Run tests
```

## Project Inspiration
When starting this project, we knew we wanted to do something finance related, but weren’t sure what to do. When looking at what problems most investors face, we saw that most investors make on average much lower returns than the market average. This has been proven by multiple studies, such as the Dalbar study, which generally shows that the average investor underperforms the market by a wide margin. For example, in 2018, the S&P 500 index returned -4.38%. The average equity mutual fund investor was down -9.42%. That's more than double. 

Therefore, our solution was to try to give the average investor closer to market returns. To do this, our approach was to choose substitute companies with the lowest volatility in each of the industries of the user’s current companies. We would also have other companies similar to the ones chosen by the user shown at the bottom, and the user can view their new portfolio with any of those companies as well.

## Project Details
This project will take in users' stocks and dollar amounts invested and analyze the stocks to predict future value and assess the stocks' risk according to volatility. Using the volatility score, a same-sector stock will be suggested for each holding, and future value will be predicted based on historical data for the current portfolio and the risk-averse portfolio. Lastly, similar companies will be suggested which have similar attributes to that in your portfolio. This suggestion is based on a clustering algorithm that looks at a variety of numeric features for example (dividend yield, average volume, and profit margins). 

## Data
The market data for this tool is accessed from yfinance. We made two data sets, one which has the closing price of every stock in the S&P500 in the past year which is used for our graphs and our volatility calculation. The second data set includes the information including sector, amount of employees, etc. (135 cols of data). This data set is used for the k means clustering for the stock similarity suggestion. We created these two data sets and updated them throughout the project to include the most up-to-date data. To clean the data to get rid of nan values, we decided to use the column mean to fill any nan values. Only a few nan values occurred throughout the data set since almost all of the companies had their data available for each numeric metric. We decided to use the column means instead of removing the rows, because we wanted to make sure that each company in the S&P500 was available in our data set.

## K-means clustering
The K-means clustering is used to group the user-inputted stocks with similar companies so that they can build different portfolios with companies similar to their current portfolio. The K-means algorithm assigns a cluster to each company in the S&P500 so the user can see all other companies in each entered companies cluster. To select features for this algorithm we used a correlation matrix to only include features that had less than a 0.85 correlation, in order to avoid multicollinearity. We also only used numeric features. After reducing the features, we used around 62 features. We also changed the parameters of the K-means algorithm to use k-means++ to choose the initial centroids, and we chose to use 75 different clusters. We wanted to pick a number of clusters where each cluster would include multiple companies. While it was not possible to get a perfect distribution, we found that 75 clusters gave a good distribution in terms of companies in each cluster, and reduced the amount of clusters with only one company in it. Finally, we set a random_state = 42 to have reproducible results each time we ran our algorithm. This clustering algorithm was then used in the front end to give new options to the user.

## Demo Video / Example Usage
[Watch the demo on YouTube](https://youtu.be/-_rtUkBWuj8)  
Short demo of the application in use.

## Progress Since Midterm
Since the midterm, we have continued to work on fine-tuning the models we already had, and we added the suggestion company based on a K-means clustering algorithm. We also increased usability in the front end with autofill and error checking. Users can now click the suggested company, and it will insert them into the perspective portfolio to show projections with that new company included. Midterm demo video: [Watch the demo on YouTube](https://youtu.be/J7ZJD8LqPIA)  

## Conclusion
The portfolio analysis tool successfully integrates stock data analysis, risk assessment, and investment recommendations into an easy-to-use platform and allows for the exploration of stock substitutes. By combining volatility analysis with k-means clustering, we provide users with data-driven insights for portfolio optimization, including lower-risk alternatives and similar company suggestions. The interactive interface and automated recommendations make financial analysis accessible to everyday investors, helping them make more informed investment decisions. We hope that this project can help the average investor get closer to market returns. By giving the user their substituted portfolio, their returns are expected to get to market returns. However, while this has worked for most of our testing and experimenting, we don’t expect users to get closer to market portfolios every time, so users are expected to use caution if investing in these companies. 

* Disclosure: This project should not be used for financial decisions  

