# This module is responsible for managing the symbols and their corresponding codes (inscodes)
# for the Tehran stock market. It provides functionality to convert between a symbol and its inscode.
import json
from . import config
from .download_realtime import get_price
import requests
import pandas as pd
from os import path

def symbols_dict():
    """
Reads the 'syms.json' file and returns a dictionary of stock symbols and their inscodes.

Returns:
dict: A dictionary with symbols as keys and inscodes as values.
"""

    file_path = path.join(path.dirname(__file__), 'syms.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        symbols_dict = json.load(f)

    return symbols_dict

def symbol_to_inscode(symbol):
    """
    Converts a stock symbol to its corresponding inscode.

    Parameters:
        symbol (str): The stock symbol to convert.

    Returns:
        str: The corresponding inscode if found, otherwise None.
"""

    symbols = symbols_dict()
    symbol = symbol.replace(chr(1610), 'ی').replace(chr(1603), 'ک')
    return symbols[symbol] if symbol in symbols.keys() else None

def inscode_to_symbol(inscode):
    """
    Converts an inscode to its corresponding stock symbol.

    Parameters:
        inscode (str): The inscode to convert.

    Returns:
        str: The corresponding stock symbol if found, otherwise None.
    """

    symbols = symbols_dict()
    symbols = {value: key for key, value in symbols.items()}
    return symbols[id] if id in symbols.keys() else None

def symbols_category():
    """
    Categorizes and returns Tehran stock market symbols based on market type.

    This function retrieves stock market data from a specified URL and combines it with
    real-time price data. It then categorizes the symbols into various market types and
    investment funds based on their attributes. The function handles exceptions and
    ensures that only valid data is processed.

    Returns:
        tuple: Contains DataFrames of categorized market symbols as follows:
        main_market: Symbols from the main board of the Bourse.
        otc_market: Symbols from the over-the-counter (OTC) market.
        •  base_market: Symbols from the base market with different risk levels (yellow, orange, red).
        funds: All investment funds.
        fixed_interest_funds: Fixed interest investment funds.
        other_funds: Other types of investment funds.
    """

    try:
        datas = requests.get(url= config.SYMBOLS, headers= config.HEADERS).text
        market_df = pd.read_html(datas, header=0)  [0]
    except:
        return
    real_df = get_price()
    if real_df is None:
        return
    market_df.columns = [
        "name", "code" ,"English Name", 
        "Company Code", "Company ISIN", "market", 
        "group", "type"
    ]
    market_df.set_index(market_df['code'], inplace= True)
    market_df = market_df[['market', 'group']]
    real_df = real_df[real_df['code'].notnull()]
    real_df['id'] = real_df.index
    real_df.set_index(real_df['code'], inplace= True)
    real_df = real_df[['id', 'code', 'symbol', 'name']]
    real_df['symbol'] = real_df['symbol'].str.replace(chr(1610), 'ی')
    real_df['symbol'] = real_df['symbol'].str.replace(chr(1603), 'ک')
    real_df = pd.concat([real_df, market_df], axis= 1)
    real_df = real_df[(real_df['id'].notnull()) & (real_df['code'].str[:3] != 'IRR')]
    first_market_main_board_bourse = real_df[real_df['market'] == "بازار اول (تابلوي اصلي) بورس"]
    first_market_secondary_board_bourse = real_df[real_df['market'] == "بازار اول (تابلوي فرعي) بورس"]
    second_market_main_board_bourse = real_df[real_df['market'] == "بازار دوم بورس"]
    main_market = pd.concat([first_market_main_board_bourse, first_market_secondary_board_bourse, second_market_main_board_bourse])
    first_market_otc = real_df[real_df['market'] == "بازار اول فرابورس"]
    second_market_otc = real_df[real_df['market'] == "بازار دوم فرابورس"]
    third_market_otc = real_df[real_df['market'] == "بازار سوم فرابورس"]
    otc_market = pd.concat([first_market_otc, second_market_otc, third_market_otc])
    base_market_yellow_otc = real_df[real_df['market'] == "بازار پايه زرد فرابورس"]
    base_market_orange_otc = real_df[real_df['market'] == "بازار پايه نارنجي فرابورس"]
    base_market_red_otc = real_df[real_df['market'] == "بازار پايه قرمز فرابورس"]
    base_market = pd.concat([base_market_yellow_otc, base_market_orange_otc, base_market_red_otc])
    market = pd.concat([main_market, otc_market, base_market])
    funds = real_df[real_df['group'] == "صندوق سرمايه گذاري قابل معامله"]
    fixed_interest_funds = funds[funds['name'].str.contains('ثا', na= False)]
    other_funds = funds[~funds['name'].str.contains('ثا', na= False)]
    return (
        main_market, otc_market, base_market,
        funds, fixed_interest_funds, other_funds
    )