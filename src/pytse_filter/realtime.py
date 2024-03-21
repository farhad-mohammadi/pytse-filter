# This module contains classes for managing real time data conditions and operations
# for the pytse_filter project.

from . import config
from .download_realtime import combine_realtime
import re
import pandas as pd

class RealTimeCondition:
    """
    This class represents a condition that the user has for filtering the stock data. It has attributes for the raw text of the condition, the file path of the condition, the last error occurred, and the converted Python code of the condition.
    """

    def __init__(self, rau_text= None, file_path= None):
        """
        This method initializes a Condition object with the given raw text or file path of the condition. If both are given, the file path is ignored.

        Parameters:
            rau_text (str): The raw text of the condition, in a custom syntax.
            file_path (str): The file path of the condition, where the raw text is stored.
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
        This method saves the raw text of the condition to the given file path.

        Parameters:
            file_path (str): The file path to save the condition.
        """

        with open(file_path, 'w') as f:
            f.write(self.rau_text)

    def load_file(self, file_path):
        """
        This method loads the raw text of the condition from the given file path and assigns it to the rau_text attribute.

        Parameters:
            file_path (str): The file path to load the condition from.
        """

        with open(file_path, 'r') as f:
            self.rau_text = f.read()
            self.is_valid()

    def convert(self):
        """
        This method converts the raw text of the condition to a valid Python code that can be applied to a pandas data frame. It uses the config.CONVERT_DICT to replace the custom syntax with the corresponding pandas syntax. It stores the converted code in the py_code attribute.
        """

        rau_text = self.rau_text
        for key, value in config.REALTIME_CONVERT_DICT.items():
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
        df = config.REALTIME_CHECK_DF
        df = eval(f'df{self.py_code}')
        return True

    def __str__(self):
        """
        This method returns the string representation of the Condition object, which is the raw text of the condition.
        
        Returns:
            rau_text (str): The raw text of the condition.
        """

        return self.rau_text


class RealTime:
    """
    This class represents a market that contains the stock data and the condition for filtering the data. It has attributes for the condition, the data frame of all the stocks, and the data frame of the filtered stocks.
    """

    def __init__(self, condition= None):
        """
        This method initializes a Market object with the given condition.

        Parameters:
            conditions (Condition): The condition object for filtering the stock data.
        """

        self.condition = condition
        self.datas = None
        self.filtered_symbols = None
        self.download_status = False
    
    def download(self):
        """
        This method loads the stock data from the web source and stores it in the datas attribute as a pandas data frame. 
        """

        self.datas = combine_realtime()
        if not self.datas is None:
            self.download_status = True
        
    def all(self, update_data = True):
        """
        This method returns the data frame of all the stocks. It optionally updates the data from the web source before returning it.
        
        Parameters:
            update_data (bool): Whether to update the data from the web source or not. Default is True.

        Returns:
            datas (pd.DataFrame): The data frame of all the stocks.
        """

        if update_data: 
            self.download()
        return self.datas
    
    def filter_by_obj_condition(self, update_data= True):
        """
        This method returns the data frame of the filtered stocks based on the condition. It optionally updates the data from the web source before filtering it. It also stores the filtered data frame in the filtered_symbols attribute.

        Parameters:
            update_data (bool): Whether to update the data from the web source or not. Default is True.

        Returns:
            filtered_symbols (pd.DataFrame): The data frame of the filtered stocks.
        """

        if update_data:
            self.download()
        df = self.datas
        if df is None :
            return pd.DataFrame()
        df = eval(f'df{self.condition.py_code}')
        self.filtered_symbols = df[df['symbol'].notnull()]
        return self.filtered_symbols

    def filter_by_text_condition(self, text_condition):
        """
        Filters the stock data based on a text condition provided as input.

        Parameters:
            text_condition (str): The raw text of the condition in custom syntax.

        Returns:
            pd.DataFrame: The filtered DataFrame of stock data.
        """

        condition = RealTimeCondition(rau_text= text_condition)
        self.condition = condition
        self.filtered_symbols = self.filter_by_obj_condition()
        return self.filtered_symbols

    def __str__(self):
        """
        This method returns the string representation of the Market object, which is the string representation of the data frame of all the stocks.
        
        Returns:
            datas (str): The string representation of the data frame of all the stocks.
        """

        return self.datas.__str__()

