import csv
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def create_clusters():
    df = pd.read_csv('CSVs/sp500_tickers_full_info.csv')
    numeric_columns = df.select_dtypes(include=['number'])
    df_numeric = df[['Ticker','sector']].join(df.select_dtypes(include=['number']))
    df_numeric = df_numeric.replace([np.inf, -np.inf], np.nan)
    # Select only numeric columns and fill NaNs with their mean
    numeric_cols = df_numeric.select_dtypes(include=["number"])
    df_numeric[numeric_cols.columns] = numeric_cols.fillna(numeric_cols.mean())

    numeric_features = df_numeric.drop(columns=["Ticker", "sector"])
    correlation_matrix = numeric_features.corr().abs()

    # Select upper triangle of correlation matrix
    upper_triangle = correlation_matrix.where(
        np.triu(np.ones(correlation_matrix.shape), k=1).astype(bool)
    )

    # Find features with correlation > 0.85 (adjust threshold as needed)
    high_correlation_features = [
        column for column in upper_triangle.columns if any(upper_triangle[column] > 0.85)
    ]

    # Drop highly correlated features
    numeric_features_reduced = numeric_features.drop(columns=high_correlation_features)

    ###Kmeans
    # Scale numeric features
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(numeric_features_reduced)

    # Apply K-Means clustering
    kmeans = KMeans(n_clusters=75, init="k-means++", random_state=42)
    df_numeric["Cluster"] = kmeans.fit_predict(scaled_features)

    df_numeric_with_cluster = df[["Ticker", "sector"]].join(df_numeric[["Cluster"]])

    return df_numeric_with_cluster

def SimiliarCompany(ticker, cluster_df):

    company_cluster = cluster_df[cluster_df['Ticker'] == ticker]['Cluster'].iloc[0]
    companies_in_cluster = cluster_df[cluster_df['Cluster'] == company_cluster]
    similiar_companies_list = companies_in_cluster['Ticker'].tolist()

    company_industry = cluster_df[cluster_df['Ticker'] == ticker]['sector'].iloc[0]
    companies_in_Sector = companies_in_cluster[companies_in_cluster['sector'] == company_industry]
    similiar_sector_list = companies_in_Sector['Ticker'].tolist()

    if ticker in similiar_companies_list:
        similiar_companies_list.remove(ticker)
    if ticker in similiar_sector_list:
        similiar_sector_list.remove(ticker)

    return similiar_companies_list
