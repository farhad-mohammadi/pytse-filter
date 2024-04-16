# This module contains functions to download and process historical stock data.

import requests
import json
import pandas as pd
from .syms_manager import symbols_dict, symbol_to_inscode
from . import config
from .calculate_client_data import calculate_client_data
from .calculate_indicators import calculate_indicators
import jdatetime
import warnings
warnings.filterwarnings('ignore' , category= FutureWarning)

def get_adjusted_price_history(symbol= None, inscode=None, length= 200):
    """
    Retrieves adjusted price history for a given stock symbol or inscode.

    Parameters:
        symbol (str): The stock symbol.
        inscode (str): The stock inscode.
        length (int): Number of records to retrieve.

    Returns:
        DataFrame: A DataFrame containing the price history.
    """

    if inscode is None :
        if symbol is None: return
        inscode =         symbol_to_inscode(symbol)
        if inscode is None : return
    try:
        datas = requests.get(config.ADJUSTED_PRICE_HISTORY.format(inscode), headers= config.HEADERS, timeout= 3).text.split(';')
    except Exception as e:
        return e
    rows = []
    for data in datas:
        rows.append(data.split(','))
    if len(rows) == 0 : return
    columns = ['date',  'high', 'low', 'open', 'close', 'volume', 'adj_close']
    df = pd.DataFrame(rows, columns= columns)
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
    def jdate(x):
        """
        Convert Gregorian date to jalali date
        """

        jalali_date = jdatetime.date.fromgregorian(date= x['date'])
        return jalali_date.strftime('%Y-%m-%d')

    df['jdate'] = df.apply(func= jdate, axis= 1)
    columns = ['date', 'jdate', 'open', 'low', 'high', 'close', 'adj_close', 'volume']
    df = df[columns]
    df.set_index(df['date'], inplace= True)
    df.drop(columns= ['date'], inplace= True)
    df[columns[2:]] = df[columns[2:]].apply (pd.to_numeric, errors='coerce')
    if length == -1 : length = 0
    df = df[-length:]
    return df

def get_price_history(symbol= None, inscode=None, length= 200):
    """
    Retrieves price history for a given stock symbol or inscode.

    Parameters:
        symbol (str): The stock symbol.
        inscode (str): The stock inscode.
        length (int): Number of records to retrieve.

    Returns:
        DataFrame: A DataFrame containing the price history.
    """

    if inscode is None :
        if symbol is None: return
        inscode =         symbol_to_inscode(symbol)
        if inscode is None : return
    if length == -1 :
        length = 9999
    try:
        datas = requests.get(config.PRICE_HISTORY.format(inscode, length), headers= config.HEADERS, timeout= 3).text.split(';')
    except:
        return
    rows = []
    for data in datas[:-1]:
        if len(data.split('@')) != 10 : break
        rows.append(data.split('@'))
    if len(rows) == 0 : return
    columns = ['date', 'high', 'low', 'adj_close', 'close', 'open', 'yesterday_adj_close', 'value', 'volume', 'count']
    df = pd.DataFrame(rows, columns= columns)
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
    def jdate(x):
        """
        Convert Gregorian date to jalali date
        """

        jalali_date = jdatetime.date.fromgregorian(date= x['date'])
        return jalali_date.strftime('%Y-%m-%d')

    df['jdate'] = df.apply(func= jdate, axis= 1)
    columns = ['date', 'jdate', 'open', 'low', 'high', 'close', 'adj_close', 'volume', 'value', 'count', 'yesterday_adj_close']
    df = df[columns]
    df.set_index(df['date'], inplace= True)
    df.drop(columns= ['date'], inplace= True)
    df[columns[2:]] = df[columns[2:]].apply (pd.to_numeric, errors='coerce')
    df = df[::-1]
    return df

def get_client_history(symbol= None, inscode=None, length= 200):
    """
    Retrieves client history for a given stock symbol or inscode.

    Parameters:
        symbol (str): The stock symbol.
        inscode (str): The stock inscode.
        length (int): Number of records to retrieve.

    Returns:
        DataFrame: A DataFrame containing the client history.
    """

    if inscode is None :
        if symbol is None: return
        inscode =         symbol_to_inscode(symbol)
        if inscode is None : return
    url = config.CLIENT_HISTORY.format(inscode)
    try:
        datas = requests.get(url, headers= config.HEADERS, timeout= 5)
        df = pd.DataFrame(datas.json()['clientType'])
    except :
        return
    if len(df) == 0 : return    
    df['recDate'] = pd.to_datetime(df['recDate'], format='%Y%m%d')
    df = df[:length]
    df.columns = df.columns.str.lower()
    df.rename(columns= {'recdate': 'date'}, inplace= True)
    df.set_index(df['date'], inplace= True)
    df.drop(columns= ['date'], inplace= True)
    df = df[::-1]
    df = df.astype('float64')
    return df

def combine_history(symbol= None, inscode=None, adjusted_price= True, length= 200, calc_inds= True, calc_client= True):
    """
    Combines price and client history into a single DataFrame.

    Parameters:
        symbol (str): The stock symbol.
        inscode (str): The stock inscode.
        adjusted_price (bool): select adjusted price or not
        length (int): Number of records to retrieve.
        calc_inds (bool): Whether to calculate indicators.
        calc_client (bool): Whether to calculate client data.

    Returns:
        DataFrame: A DataFrame containing the combined history.
    """

    if adjusted_price:
        price_df = get_adjusted_price_history(symbol= symbol, inscode=inscode, length= length)
    else:
        price_df = get_price_history(symbol= symbol, inscode=inscode, length= length)
    if price_df is None :
        return
    client_df = get_client_history(symbol= symbol, inscode=inscode, length= length)
    if client_df is None:
        return
    if calc_inds:
        price_df = calculate_indicators(price_df)
    if calc_client:
        client_df = calculate_client_data(client_df)
    df = pd.concat([price_df, client_df], axis= 1, sort= True)
    return df

