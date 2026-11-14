"""Utility functions for correlation analysis between SPI and cereal production."""

import pandas as pd
import numpy as np


def add_anomaly(df, colname):
    """
    Takes a pandas dataframe with a Country Name column and finds the anomaly 
    and a normalized anomaly of the column given by "colname".
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame containing cereal production data with 'Country Name' column
    colname : str
        Name of the column to calculate anomalies for
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with added columns: '{colname}_Mean', 'Anomaly', 
        '{colname}_Std', and 'Anomaly_Normalized'
    """
    # Calculate mean production by country
    mean_production_country = df.groupby('Country Name')[colname].mean().reset_index()
    mean_production_country = mean_production_country.rename(columns={colname: colname + '_Mean'})
    df = df.merge(mean_production_country, on='Country Name')
    
    # Calculate anomaly
    df['Anomaly'] = df[colname] - df[colname + '_Mean']
    
    # Calculate standard deviation for each country
    std_by_country = df.groupby('Country Name')[colname].std().reset_index()
    std_by_country = std_by_country.rename(columns={colname: colname + '_Std'})
    
    # Merge standard deviation
    df = df.merge(std_by_country, on='Country Name')
    
    # Normalize anomaly (Z-score)
    df['Anomaly_Normalized'] = df['Anomaly'] / df[colname + '_Std']
    
    return df


def prep_corr(df, spi_df, country):
    """
    Takes a pandas dataframe with a "Country Name" column and a country name 
    found within the "Country Name" column and provides a joined truncated 
    dataframe of the relevant columns.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame containing cereal production data with 'Country Name' and 'Year' columns
    spi_df : pd.DataFrame
        DataFrame containing SPI data with 'year' index
    country : str
        Country name to filter for (e.g., 'Indonesia', 'Viet Nam')
        
    Returns:
    --------
    pd.DataFrame
        Joined dataframe with SPI and cereal data for the specified country,
        truncated to years <= 2023
    """
    new_df = df.loc[df['Country Name'] == country].set_index('Year')
    new_df.index.name = 'year'
    new_df.index = new_df.index.astype('int')
    new_df = spi_df.join(new_df)
    new_df = new_df.loc[:2023, :]
    return new_df


def calculate_pearson_correlation(spi_series, anomaly_series):
    """
    Calculate Pearson correlation coefficient and p-value between SPI and anomaly.
    
    Parameters:
    -----------
    spi_series : array-like
        SPI values
    anomaly_series : array-like
        Anomaly values (e.g., normalized cereal production anomaly)
        
    Returns:
    --------
    tuple
        (correlation_coefficient, p_value)
    """
    from scipy.stats import pearsonr
    return pearsonr(spi_series, anomaly_series)


def analyze_drought_category_impact(df, category_col='category', value_col='Anomaly_Normalized'):
    """
    Analyze the impact of drought categories on cereal production anomalies.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame containing SPI categories and anomaly data
    category_col : str
        Name of the column containing drought categories
    value_col : str
        Name of the column containing anomaly values
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with mean and median anomaly values by drought category
    """
    return df.groupby(category_col)[value_col].agg(['mean', 'median'])
