# This module is responsible for managing the symbols and their corresponding codes (inscodes)
# for the Tehran stock market. It provides functionality to convert between a symbol and its inscode.
import json
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

