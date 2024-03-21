# This module is designed to fetch and process real-time stock market data. 
# It includes functions to retrieve supply and demand data, price data, and client transaction data from specified URLs. The data is then processed into pandas DataFrames, which are combined to provide a comprehensive view of the market activity.

import requests  
import pandas as pd
from . import config

def get_supply_demand_data(datas):
    """
    This function takes a string input that contains the data related to the supply and demand queues, and returns a pandas data frame that has columns for the zone, the depth, the price, and the quantity of each row and each stock.
    
    Parameters:
        datas (str): A string that contains the data related to the supply and demand queues, separated by '@' and ';'.

    Returns:
        df (pd.DataFrame): A pandas data frame that has columns for the zone, the depth, the price, and the quantity of each row and each stock.
"""

    try:
        datas = datas.split('@')[3].split(';')
    except:
        return
    if len(datas) < 100 : return 
    rows = []
    for data in datas:
        sub_data = data.split(',')
        if len(sub_data) == 8 :
            rows.append(sub_data)
    if len(rows) < 100 : return 
    df = pd.DataFrame(rows)
    df.columns =['id', 'row', 2, 3, 4, 5, 6, 7]
    df.set_index(df['id'], inplace= True)
    df.drop(columns=['id'], inplace= True)
    groups = df.groupby('row')
    df1 = groups.get_group('1')
    df1.columns=['row', 'zo1', 'zd1', 'pd1', 'po1', 'qd1', 'qo1']
    df2 = groups.get_group('2')
    df2.columns=['row', 'zo2', 'zd2', 'pd2', 'po2', 'qd2', 'qo2']
    df3 = groups.get_group('3')
    df3.columns=['row', 'zo3', 'zd3', 'pd3', 'po3', 'qd3', 'qo3']
    df4 = groups.get_group('4')
    df4.columns=['row', 'zo4', 'zd4', 'pd4', 'po4', 'qd4', 'qo4']
    df5 = groups.get_group('5')
    df5.columns=['row', 'zo5', 'zd5', 'pd5', 'po5', 'qd5', 'qo5']
    df = pd.concat([df1, df2, df3, df4, df5], axis=1)
    df.drop(columns= ['row'], inplace= True)
    return df

def get_price():
    """
    This function requests the data from a web link specified in the config file, and calls the get_supply_demand_data function to process the data related to the supply and demand queues. 
    It also separates the data related to the price data of different stocks, and returns a pandas data frame that has columns for the code, 
    the symbol, the name, the final price, the closing price, the last price, the trade volume, the trade value, the minimum price, the maximum price, the yesterday price, the EPS, the base volume, the maximum threshold, and the minimum threshold of each stock. 
    It also calculates the percentage change of the closing price and the last price from the yesterday price, and adds them as columns to the data frame.

    Parameters:
        None

    Returns:
        df (pd.DataFrame): A pandas data frame that has columns for the code, 
        the symbol, the name, the final price, the closing price, the last price, the trade volume, the trade value, the minimum price, the maximum price, the yesterday price, the EPS, the base volume, the maximum threshold, and the minimum threshold of each stock, as well as the percentage change of the closing price and the last price from the yesterday price.
    """

    try:
        datas=requests.get(config.PRICE_URL, headers= config.HEADERS, timeout= 3).text
    except:
        return
    rows_df = get_supply_demand_data(datas)
    if rows_df is None: return
    datas = datas.split(';')
    if len(datas) < 100 : return 
    data23 = []
    data25 = []
    for data in datas:
        sub_data = data.split(',')
        if len(sub_data) == 23 : 
            data23.append(sub_data)
        elif len(sub_data) == 25 : 
            data25.append(sub_data)
    if len(data23) < 100 and len(data25) < 100: return
    if len(data23) > 100 :
        df = pd.DataFrame(data23)
        df.columns = ['id', 'code', 'symbol', 'name', 'nc', 'pf', 'pc', 'pl', 'nc', 'tvol', 'tval',
        'pmin', 'pmax', 'py', 'eps', 'bvol', 'nc', 'nc', 'nc', 'tmax', 'tmin', 'nc', 'nc']
    else:
        df = pd.DataFrame(data25)
        df.columns = ['id', 'code', 'symbol', 'name', 'nc', 'pf', 'pc', 'pl', 'nc', 'tvol', 'tval',
        'pmin', 'pmax', 'py', 'eps', 'bvol', 'nc', 'nc', 'nc', 'tmax', 'tmin', 'nc', 'nc', 'nc', 'nc']
    df = df[~df['symbol'].str.contains(r'\d')]
    df.set_index(df['id'], inplace= True)
    df.drop(columns=['id', 'nc'], inplace= True)
    df = pd.concat([df, rows_df], axis= 1)
    cols = df.columns[3:]
    df[cols] = df[cols].apply (pd.to_numeric, errors='coerce')
    df['pcp'] = (100 * (df['pc'] - df['py']) / df['py']).round(2)
    df['plp'] = (100 * (df['pl'] - df['py']) / df['py']).round(2)
    df['pfp'] = (100 * (df['pf'] - df['py']) / df['py']).round(2)
    df['pminp'] = (100 * (df['pmin'] - df['py']) / df['py']).round(2)
    df['pmaxp'] = (100 * (df['pmax'] - df['py']) / df['py']).round(2)
    df['tminp'] = (100 * (df['tmin'] - df['py']) / df['py']).round(2)
    df['tmaxp'] = (100 * (df['tmax'] - df['py']) / df['py']).round(2)
    return df

def get_client():
    """
    This function requests the data from another web link specified in the config file, and separates the data related to the purchase and sales information of different stocks. 
    It returns a pandas data frame that has columns for the buy individual count, the buy non-individual count, the buy individual volume, the buy non-individual volume, the sell individual count, the sell non-individual count, the sell individual volume, and the sell non-individual volume of each stock. 

    Parameters:
        None

    Returns:
        df (pd.DataFrame): A pandas data frame that has columns for the buy individual count, the buy non-individual count, the buy individual volume, the buy non-individual volume, the sell individual count, the sell non-individual count, the sell individual volume, and the sell non-individual volume of each stock, 
        as well as the buy individual value, the sell individual value, the buy non-individual value, the sell non-individual value, the buy per capita, the sell per capita, the supply demand index, the volume, the individual buy ratio, the individual sell ratio, the non-individual buy ratio, and the non-individual sell ratio.
    """ 

    try:
        datas=requests.get(config.CLIENT_URL, headers= config.HEADERS, timeout= 3).text.split(';')
    except:
        return
    if len(datas) < 100 : return 
    client = []
    for data in datas:
        sub_data = data.split(',')
        if len(sub_data) == 9 : 
            client.append(sub_data)
    if len(client) < 100 : return 
    df = pd.DataFrame(client)
    df.columns = ['id', 'buy_i_count', 'buy_n_count', 'buy_i_volume', 'buy_n_volume', 'sell_i_count', 'sell_n_count', 'sell_i_volume', 'sell_n_volume']
    df.set_index(df['id'], inplace= True)
    df.drop(columns=['id'], inplace= True)
    df = df.apply (pd.to_numeric, errors='coerce')
    return df

def combine_realtime():
    """
    This function calls the get_price and the get_client functions, and combines their data frames by joining them on the id column. 
    It returns a pandas data frame that has all the columns from the previous data frames, and filters out the rows that have null values in the symbol column.
    It also calculates the buy individual value, the sell individual value, the buy non-individual value, the sell non-individual value, the buy per capita, the sell per capita, the supply demand index, the volume, the individual buy ratio, the individual sell ratio, the non-individual buy ratio, and the non-individual sell ratio, and adds them as columns to the data frame.

    Parameters:
        None

    Returns:
        df (pd.DataFrame): A pandas data frame that has all the columns from the previous data frames, and filters out the rows that have null values in the symbol column.
    """

    price_df = get_price()
    if price_df is None : return
    client_df = get_client()
    if client_df is None : return
    df = pd.concat([price_df, client_df], axis= 1)
    df['buy_i_value'] = df['pc'] * df['buy_i_volume']
    df['sell_i_value'] = df['pc'] * df['sell_i_volume']
    df['buy_n_value'] = df['pc'] * df['buy_n_volume']
    df['sell_n_value'] = df['pc'] * df['sell_n_volume']
    df['buy_per_capita'] = (df['buy_i_value'] / df['buy_i_count'] / 10000000 ).round(1)
    df['sell_per_capita'] = (df['sell_i_value'] / df['sell_i_count'] / 10000000 ).round(1)
    df['power_of_demand'] = (df['buy_per_capita'] / df['sell_per_capita']).round(2)
    df['volume'] = df['buy_i_volume'] + df['buy_n_volume']
    df['ind_buy_ratio'] = (100 * df['buy_i_volume'] / df['volume'] ).round(1)
    df['ind_sell_ratio'] = (100 * df['sell_i_volume'] / df['volume'] ).round(1)
    df['cor_buy_ratio'] = (100 * df['buy_n_volume'] / df['volume'] ).round(1)
    df['cor_sell_ratio'] = (100 * df['sell_n_volume'] / df['volume'] ).round(1)
    df['indivisual_mony_flow'] = df['buy_i_value'] - df['sell_i_value']
    df = df[df['symbol'].notnull()]
    df = df[config.REALTIME_COLUMNS]
    return df