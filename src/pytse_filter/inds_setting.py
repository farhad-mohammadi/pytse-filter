# This module defines the settings for various technical analysis indicators.
# It contains a dictionary named 'indicators' which outlines the calculation details
# for each technical indicator used in the analysis.

indicators = {
    "rsi": [
        {
            'columns':[
                'rsi'
            ],
            'args':{
                "close": "df['close']",
                "length": 14
            }
        }
    ],
    "macd":[
        {
            'columns':[
                'macd', 'histogram', 'signal'
            ],
            'args': {
                "close": "df['close']",
                "fast": 12, 
                "slow": 26, 
                "signal": 9
            }
        }
    ],
    "stoch":[
        {
            'columns':[
                'k', 'd'
            ],
            'args':{
                "close": "df['close']",
                "high": "df['high']",
                "low": "df['low']",
                "k": 5,
                "d": 3,
                "smooth_k": 3
            }
        }
    ],
    "mfi":[
        {
            'columns':[
                'mfi'
            ],
            'args':{
                "close": "df['close']",
                "high": "df['high']",
                "low": "df['low']",
                "volume": "df['volume']",
                "length": 14,
                "drift": 1
            }
        }
    ],
    "sma":[
        {
            "columns": [
                "sma50"
            ],
            "args":{
                "close": "df['close']",
                "length": 50
            }
        },
        {
            "columns": [
                "sma21"
            ],
            "args":{
                "close": "df['close']",
                "length": 21
            }
        }
    ],
    "ema":[
        {
            "columns":[
                "ema21"
            ],
            "args":{
                "close": "df['close']",
                "length": 21
            }
        }
    ],
    "stochrsi":[
        {
            "columns":[
                "rsi_k", "rsi_d"
            ],
            "args":{
                "close": "df['close']",
                "length": 14,
                "rsi_length": 14,
                "k": 3,
                "d": 3
            }
        }
    ],
    "bbands":[
        {
            "columns":[
                "lower_band", "mid_band", "upper_band", "band_width", "band_percent"
            ],
            "args":{
                "close": "df['close']",
                "length": 5,
                "std": 2
            }
        }
    ],
    "ichimoku":[
        {
            "columns":[
                ["spana", "spanb", "tenkan", "kijun"],
                ["future_spana","future_spanb"]
            
            ],
            "args":{
                "close": "df['close']",
                "high": "df['high']",
                "low": "df['low']",
                "tenkan": 9,
                "kijun": 26,
                "senkou": 52,
                "include_chikou": False
            }
        }
    ],
    "max":[
        {
            "columns": [
                "highest21"
            ],
            "args": {
                "source": "df['high']",
                "period": 21
            }
        },
        {
            "columns": [
                "highest63"
            ],
            "args": {
                "source": "df['high']",
                "period": 63
            }
        }
    ],
    "min":[
        {
            "columns": [
                "lowest21"
            ],
            "args": {
                "source": "df['low']",
                "period": 21
            }
        },
        {
            "columns": [
                "lowest63"
            ],
            "args": {
                "source": "df['low']",
                "period": 63
            }
        }
    ],
    # ... other indicators ...
}

def maximum(d, max_value):
    """
    Recursively find the maximum value in a nested dictionary.

    Parameters:
        d (dict): The dictionary to search.
        max_value (int/float): The current maximum value found.

    Returns:
        int/float: The maximum value found.
    """

    for k, v in d.items():
        if isinstance(v, dict):
            max_value = maximum(v, max_value)
        if isinstance(v, (int, float)):
            if v > max_value:
                max_value = v
    return max_value

def find_count(d):
    """
    Find the count of values in a nested dictionary that exceed a predefined maximum.

    Parameters:
        d (dict): The dictionary to search.

    Returns:
        int: The count of values exceeding the maximum.
    """

    max_value = 100
    for  key, values in d.items():
        for value in values:
            max_value = maximum(value, max_value)
    return max_value + 100
