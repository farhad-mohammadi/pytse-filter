# This module contains classes for managing historical data conditions and operations
# for the pytse_filter project.

from . import config
from .download_history import combine_history
from .syms_manager import symbols_dict
from . import inds_setting 
import re
import pandas as pd
from tqdm import tqdm
from os import path, mkdir

class HistoryCondition:
    """
    A class to manage and validate conditions for filtering historical stock data.
    """

    def __init__(self, rau_text= None, file_path= None):
        """
        Initializes the HistoryCondition object with either raw text or a file path containing the condition.

        Parameters:
            rau_text (str): The raw text of the condition in custom syntax.
            file_path (str): The path to a file containing the condition text.
        """

        self.rau_text = rau_text
        self.py_code = None
        if not file_path is None:
            with open(file_path, 'r') as f:
                self.rau_text = f.read()
        if not self.rau_text is None:
            self.rau_text = self.rau_text.lower()
            self.is_valid()

    def save(self, file_path):
        """
        Saves the raw text of the condition to a specified file.

        Parameters:
            file_path (str): The path to the file where the condition text will be saved.
        """

        with open(file_path, 'w') as f:
            f.write(self.rau_text)

    def load_file(self, file_path):
        """
        Loads the condition text from a specified file and validates it.

        Parameters:
            file_path (str): The path to the file from which to load the condition text.
        """

        with open(file_path, 'r') as f:
            self.rau_text = f.read()
            self.is_valid()

    def convert(self):
        """
        Converts the raw text of the condition into executable Python code for data filtering.
        """

        rau_text = self.rau_text
        for key, value in config.HISTORY_CONVERT_DICT.items():
            pattern = r"\b" + key + r"\b"
            rau_text = re.sub(pattern, value, rau_text)
        parts = re.split(r'\b(and|or)\b', rau_text)
        parts = map(lambda x: x.strip(), parts)
        change_dict = {'and': ' & ', 'or': ' | '}
        self.py_code = ''
        for part in parts:
            self.py_code += f'({part})' if ( part != 'and' and part != 'or' ) else change_dict[part]
        self.py_code = f'.loc[({self.py_code})]'

    def is_valid(self):
        """
        Validates the condition by attempting to execute the generated Python code.

        Returns:
            bool: True if the condition is valid, False otherwise.
        """

        self.convert()
        df = config.HISTORY_CHECK_DF()
        df = eval(f'df{self.py_code}')
        return True

    def __str__(self):
        """
Returns the raw text of the condition.

Returns:
str: The raw text of the condition.
"""

        return self.rau_text


class History:
    """
    A class to handle downloading, summarizing, and filtering historical stock data
    based on specified conditions.
    """

    def __init__(self, condition= None, base_path= 'history\\'):
        """
        Initializes the History object with an optional condition for filtering stock data and a base path for saving files.

        Parameters:
            condition (HistoryCondition): An object representing the filter condition.
            base_path (str): The base directory path where files will be saved.
        """

        self.condition = condition
        self.datas = None
        self.filtered_symbols = None
        self.download_status = False
        self.base_path = base_path
        if not path.exists(self.base_path):
            mkdir(self.base_path)
        self.num_of_all_symbols = None
        self.num_of_success = None
    def download_summery(self, symbols= "all", adjusted_price= True):
        """
        Downloads and summarizes historical data for a list of symbols or all symbols if not specified.

        Parameters:
            symbols (list/str): A list of symbols to summarize or "all" to summarize all symbols.
            adjusted_price (bool): download adjusted price or not

        Returns:
            pd.DataFrame: A DataFrame containing the summarized historical data.
        """

        if symbols == "all":
            symbols = list(symbols_dict().keys())
        dfs = []
        length = inds_setting.find_count(inds_setting.indicators)
        for symbol in tqdm(symbols):
            df = combine_history(symbol, adjusted_price= adjusted_price, length= length)
            if not df is None:
                df0 = df.loc[[df.index[-1]]]
                df1 =  df.loc[[df.index[-2]]]
                df1.set_index(df0.index, inplace= True)
                df1.rename(columns= lambda x: 'y_' + x, inplace= True)
                df = pd.concat([df0, df1], axis= 1)
                df.set_index(pd.Series([symbol], name= 'symbol'), inplace= True)
                dfs.append(df)
        if len(dfs) > 0:
            result = pd.concat(dfs)
            self.download_status = True
            self.num_of_success = len(dfs)
            self.num_of_all_symbols = len(symbols)
            result.to_csv(self.base_path + 'summery.csv')
            return result

    def download_history(self, symbol, adjusted_price= True, length= -1, calc_inds= True, calc_client= True, save_excel_file= True):
        """
        Downloads and saves historical data for a specific symbol to an Excel file.

        Parameters:
            symbol (str): The stock symbol to download historical data for.
            adjusted_price (bool): download adjusted price or not
            length (int): The number of days of historical data to download.
            calc_inds (bool): Whether to calculate indicators for the data.
            calc_client (bool): Whether to calculate client data for the data.
            save_excel_file (bool): save result to an excel file or not

        Returns:
            pd.DataFrame: A DataFrame containing the historical data.
        """

        df = combine_history(symbol= symbol, adjusted_price= adjusted_price, length= length, calc_inds= calc_inds, calc_client= calc_client)
        if df is None:
            return
        df.drop(columns= ['inscode'], inplace= True)
        df = df[::-1]
        if save_excel_file:
            df.to_excel(f"{self.base_path}{symbol}.xlsx")
        return df
    
    def filter_by_obj_condition(self):
        """
        Filters the summarized historical data based on the object's condition attribute.

        Returns:
            pd.DataFrame: The filtered DataFrame of historical data.
        """

        if not path.isfile(self.base_path + 'summery.csv'):
            raise FileNotFoundError('The file summery.csv was not found, To filter symbols, the download method must be called first.')
        df = pd.read_csv( self.base_path + 'summery.csv', index_col= 'symbol')
        if df is None :
            return pd.DataFrame()
        df = eval(f'df{self.condition.py_code}')
        self.filtered_symbols = df#[df['symbol'].notnull()]
        return self.filtered_symbols

    def filter_by_text_condition(self, text_condition):
        """
        Filters the summarized historical data based on a text condition provided as input.

        Parameters:
            text_condition (str): The raw text of the condition in custom syntax.

        Returns:
            pd.DataFrame: The filtered DataFrame of historical data.
        """

        condition = HistoryCondition(rau_text= text_condition)
        self.condition = condition
        self.filtered_symbols = self.filter_by_obj_condition()
        return self.filtered_symbols
    def __str__(self):
        """
        Returns a string representation of the History object, summarizing its current state.
        """
        if self.download_status:
            summary = "History data downloaded\n"
            summary += f"{self.num_of_success} of {self.num_of_all_symbols} downloaded succesfully."
        else:
            summary = "No historical data has been downloaded yet."
        return summary
