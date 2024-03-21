# This module contains the function to calculate client-specific financial data
# for the pytse_filter project. It uses settings from the client_setting module
# to perform rolling calculations on the provided DataFrame.

from . import client_setting

def calculate_client_data(df):
    """
    Calculates per capita buy and sell values, power of demand, and individual money flow
    for each row in the DataFrame. Also applies rolling calculations as defined in the
    client_setting module.

    Parameters:
    df (DataFrame): The DataFrame containing the stock market data.

    Returns:
        DataFrame: The DataFrame with additional calculated columns.
    """

    df['buy_per_capita'] = (df['buy_i_value'] / df['buy_i_count']) / 10000000
    df['sell_per_capita'] = (df['sell_i_value'] / df['sell_i_count']) / 10000000    
    df['power_of_demand'] = df['buy_per_capita'] / df['sell_per_capita']
    df['indivisual_mony_flow'] = (df['buy_i_value'] - df['sell_i_value']) / 10000000
    for calc_name, calc_sets in client_setting.calculations.items():
        for calc_set in calc_sets:
            df[calc_set['columns'][0]] = eval(f"df['{calc_name}'].rolling({calc_set['args']['period']}).{calc_set['args']['method']}()")
    return df