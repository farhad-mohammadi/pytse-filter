# This module contains the function to calculate various technical analysis indicators
# for the pytse_filter project. It uses settings from the inds_setting module
# to apply technical analysis functions on the provided DataFrame.

import pandas as pd
import pandas_ta as ta
from . import inds_setting

def calculate_indicators(df):
    """
    Applies technical analysis indicator calculations to the provided DataFrame.
    The calculations are based on the settings defined in the inds_setting module.

    Parameters:
        df (DataFrame): The DataFrame containing the stock market data.

    Returns:
        DataFrame: The DataFrame with additional columns for each indicator calculated.
    """

    for ind_name, ind_sets  in inds_setting.indicators.items():
        if ind_name not in ['min', 'max']:
            for i, ind_set in enumerate(ind_sets):
                args = ', '.join([f'{k}= {v}' for k, v in ind_set['args'].items()])
                temp_df = eval(f"ta.{ind_name}({args})")
                if isinstance(temp_df, pd.DataFrame):
                    temp_df.columns = ind_set['columns']
                    df =pd.concat([df, temp_df], axis= 1)
                elif isinstance(temp_df, pd.Series):
                    df[ind_set['columns'][0]] = temp_df
                elif ind_name == "ichimoku":
                    ichi = temp_df[0]
                    future_ichi = temp_df[1]
                    if ichi is not None:
                        ichi.columns = ind_set['columns'][0]
                        future_ichi.columns = ind_set['columns'][1]                
                        future_ichi.set_index(ichi.index[-inds_setting.indicators[ind_name][i]['args']['kijun']:], inplace= True)
                    else:
                        ichi = pd.DataFrame(columns= ind_set['columns'][0])
                        future_ichi = pd.DataFrame(columns= ind_set['columns'][1]                )
                    df =pd.concat([df, ichi, future_ichi], axis= 1)
        else:
            for i, ind_set in enumerate(ind_sets):
                df[ind_set['columns'][0]] = eval(f"{ind_set['args']['source']}.rolling({ind_set['args']['period']}).{ind_name}()")
                df["dis_from" + ind_set['columns'][0]] =  100 * (
                    df['close'] - df[ind_set['columns'][0]]).abs(
                ) / df[ind_set['columns'][0]]
    return df