"""
Configuration settings for the pytse-filter project.

This module contains constants and configurations used throughout the pytse-filter project,
including URLs for data sources, HTTP headers for requests, and column names for data processing.

Attributes:
HEADERS (dict): Headers to use for HTTP requests.
PRICE_URL (str): URL to fetch real-time price data.
CLIENT_URL (str): URL to fetch real-time client type data.
PRICE_HISTORY (str): URL template to fetch historical price data.
CLIENT_HISTORY (str): URL template to fetch historical client type data.
REALTIME_COLUMNS (list): List of column names for real-time data.
REALTIME_CHECK_DF (DataFrame): Dummy DataFrame for checking real-time data columns.
REALTIME_CONVERT_DICT (dict): Dictionary for converting real-time data columns.
HISTORY_COLUMNS (list): List of column names for historical data.
HISTORY_CHECK_DF (function): Function to generate a dummy DataFrame for historical data.
HISTORY_CONVERT_DICT (dict): Dictionary for converting historical data columns.
"""

import pandas as pd
from .calculate_indicators import calculate_indicators
from .calculate_client_data import calculate_client_data

HEADERS  = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
PRICE_URL = "http://old.tsetmc.com/tsev2/data/MarketWatchPlus.aspx"
CLIENT_URL = "http://old.tsetmc.com/tsev2/data/clienttypeall.aspx"
PRICE_HISTORY = "http://old.tsetmc.com/tsev2/data/InstTradeHistory.aspx?i={}&Top={}&A=0"
CLIENT_HISTORY ="http://cdn.tsetmc.com/api/ClientType/GetClientTypeHistory/{}"

REALTIME_COLUMNS = [
    'code', 'symbol', 'name', 'pf', 'pmin', 'pmax', 'pl', 'pc', 'py', 'tno', 'tvol', 'tval',
    'eps', 'bvol', 'tmax', 'tmin', 
    'plp', 'pcp', 'pfp', 'pminp', 'pmaxp', 'tminp', 'tmaxp',  'z',
    'buy_i_count', 'buy_n_count',
    'buy_i_volume', 'buy_n_volume', 'sell_i_count', 'sell_n_count',
    'sell_i_volume', 'sell_n_volume', 'buy_i_value',
    'sell_i_value', 'buy_n_value', 'sell_n_value', 'buy_per_capita',
    'sell_per_capita', 'power', 'volume', 'ind_buy_ratio',
    'ind_sell_ratio', 'cor_buy_ratio', 'cor_sell_ratio', 'mony_flow',
    'd1_value', 'o1_value',
    'zo1', 'zd1', 'pd1', 'po1', 'qd1', 'qo1', 
    'zo2', 'zd2', 'pd2', 'po2', 'qd2', 'qo2', 'zo3', 'zd3',
    'pd3', 'po3', 'qd3', 'qo3', 'zo4', 'zd4', 'pd4', 'po4', 'qd4', 'qo4',
    'zo5', 'zd5', 'pd5', 'po5', 'qd5', 'qo5'
]

REALTIME_CHECK_DF = pd.DataFrame({col: [1] for col in REALTIME_COLUMNS})

REALTIME_CONVERT_DICT = {col: f'df["{col}"]' for col in REALTIME_COLUMNS}

HISTORY_COLUMNS = [
    "jdate", "open", "low", "high", "close", "adj_close",
    "volume", "value", "count", "yesterday_adj_close",
    "inscode", "buy_i_volume", "buy_n_volume", "buy_i_value", "buy_n_value",
    "buy_n_count", "sell_i_volume", "buy_i_count", "sell_n_volume",
    "sell_i_value", "sell_n_value", "sell_n_count", "sell_i_count"
]

def HISTORY_CHECK_DF():
    """
    Generates a DataFrame with dummy values for historical data and applies indicator
    and client data calculations. Adds 'y_' prefix to each column name to indicate
    historical data.

    Returns:
        DataFrame: A DataFrame with calculated indicators and client data, including prefixed column names.
    """

    df = pd.DataFrame([{col: 1 for col in HISTORY_COLUMNS} for i in range(100)])
    df = calculate_indicators(df)
    df = calculate_client_data(df)
    for col in df.columns:
        df['y_' + col] = df[col]
    return df

HISTORY_CONVERT_DICT = {col: f'df["{col}"]' for col in HISTORY_CHECK_DF().columns}
