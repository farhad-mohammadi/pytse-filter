User Guide for pytse-filter
This user guide will assist you in utilizing the pytse-filter project, a Python library designed to process Tehran Stock Exchange symbol data through user-defined text filters and return the results.

Prerequisites
To use the pytse-filter library, ensure you have:

•  Python 3 installed on your system.

•  The pandas, pandas_ta, requests, and tqdm packages installed via pip.

•  The pytse-filter package installed from GitHub or PyPI.

Installation:

You can install the pytse-filter using the following methods:

pip install pytse_filter

Alternatively, for the latest version directly from the repository:

pip install git+"https://github.com/farhad-mohammadi/pytse-filter.git"

Or, clone the repository and install from the local directory:

git clone https://github.com/farhad-mohammadi/pytse-filter
cd pytse_filter
pip install .

Note: The dependent libraries will be automatically installed with the main library.

How to Use the pytse-filter Library
The pytse-filter library is divided into two main parts: Realtime and History, catering to both beginners and professionals across various departments.

Beginner Use of RealTime
Import the RealTime class from the library and pass the filter text as shown in the examples below:

from pytse_filter import RealTime

# Example 1: Symbols with more buyer power than seller power
conditions = 'pl < py and power_of_demand > 1'
df = RealTime().filter_by_text_condition(conditions)
print(df)
# Optionally save the result to an Excel file
# df.to_excel('myfilter.xlsx')

# Example 2: Symbols with high buyer-to-seller power and significant per capita purchase
conditions = 'power_of_demand > 2 and buy_per_capita > 30'
df = RealTime().filter_by_text_condition(conditions)
print(df)
# df.to_excel('myfilter.xlsx')

# Example 3: Symbols with a high actual purchase percentage and legal sale ratio
conditions = 'ind_buy_ratio > 80 and cor_sell_ratio > 50'
df = RealTime().filter_by_text_condition(conditions)
print(df)
# df.to_excel('myfilter.xlsx')

Advanced Realtime Use
For advanced users, it's possible to continuously fetch data and monitor for specific status changes in symbols:

from pytse_filter import RealTime
from time import sleep
import sys

market = RealTime()
sell_queue_symbols = market.filter_by_text_condition('pl == tmin')
if not sell_queue_symbols:
    print('No sell queues detected.')
    sys.exit()

sell_queue_symbols = sell_queue_symbols['symbol'].tolist()
print(sell_queue_symbols)

while True:
    sleep(10)  # Check every 10 seconds
    updated_sell_queue_symbols = market.filter_by_text_condition('pl == tmin')
    if updated_sell_queue_symbols is None:
        continue
    updated_sell_queue_symbols = updated_sell_queue_symbols['symbol'].tolist()
    for sym in sell_queue_symbols:
        if sym not in updated_sell_queue_symbols:
            print(f'Sell queue cleared for {sym}')
    sell_queue_symbols = updated_sell_queue_symbols

It is also possible to specify different conditions using RealTimeCondition and apply several different conditions to the data by getting the data only once using the update_data=False argument.

from pytse_filter import RealTime, RealTimeCondition
import sys

buy_queue_condition = RealTimeCondition('pl == tmax')
sell_queue_condition = RealTimeCondition('pl == tmin')
positive_conditions = RealTimeCondition('pl < tmax & plp > 1')
negative_conditions = RealTimeCondition('pl > tmin & plp < -1')
zero_condition = RealTimeCondition('plp <= 1 & plp >= -1')

market_data = RealTime()
market_data.download()
if not market_data.download_status:
    print("can't download data")
    sys.exit()

market_data.condition = buy_queue_condition
buy_queue_symbols = market_data.filter_by_obj_condition(update_data=False)

market_data.condition = sell_queue_condition
sell_queue_symbols = market_data.filter_by_obj_condition(update_data=False)

market_data.condition = positive_conditions
positive_symbols = market_data.filter_by_obj_condition(update_data=False)

market_data.condition = negative_conditions
negative_symbols = market_data.filter_by_obj_condition(update_data=False)

market_data.condition = zero_condition
zero_symbols = market_data.filter_by_obj_condition(update_data=False)

symbols_total = len(buy_queue_symbols) + len(sell_queue_symbols) + len(positive_symbols) + len(negative_symbols) + len(zero_symbols)
msg = f"""Market at a glance:
Out of {symbols_total} symbols
{len(buy_queue_symbols)} symbols in buy queue
{len(sell_queue_symbols)} symbols in sell queue
{len(positive_symbols)} symbols in positive range
{len(negative_symbols)} symbols in negative range
{len(zero_symbols)} symbols in zero range are trading."""

print(msg)  # You can send the text to your social networks.

Using the History Class
The History class in the pytse-filter library is a powerful tool for analyzing historical stock data. It enables you to apply various technical indicators and perform calculations on individual and aggregate buying and selling records.

Downloading Data
Before applying filters, you need to download and process the data for all symbols. This is done using the download_summary method:

from pytse_filter import History

# Run this after 8 pm to update the data with the latest market information
History().download_summary()

Depending on your internet speed, this process can take between 20 minutes to over an hour. However, once the data is updated, it is saved locally, allowing you to apply numerous filters quickly.

Basic Filtering
For beginners, the History class provides a straightforward way to filter symbols based on technical indicators and buying/selling patterns:

from pytse_filter import History

# Example: Symbols with an RSI less than 30 and a positive moving average convergence
conditions = 'rsi14 < 30 and macd > 0'
df = History().filter_by_text_condition(conditions)
print(df)
# Optionally save the result to an Excel file
# df.to_excel('filtered_symbols.xlsx')

Advanced Usage
Advanced users can customize indicators and settings in the inds_setting.py file. You can also use the download_history method to retrieve the history of each symbol, apply indicators and calculations, and save the results:

from pytse_filter import History

# Update the inds_setting.py file with your desired indicators and settings

# Example: Filtering symbols with a high Money Flow Index (MFI) and a bullish MACD crossover
conditions = 'mfi > 80 and macd > signal'
df = History().filter_by_text_condition(conditions)
print(df)
# Save the filtered data for further analysis
# df.to_excel('advanced_filter.xlsx')

Combining Realtime and History
For a comprehensive analysis, you can combine realtime and historical data. This allows you to track symbols that meet certain historical criteria and monitor their performance in real-time:

from pytse_filter import History, RealTime
from time import sleep

# Pre-filter symbols based on historical RSI being below 40
historical_symbols = History().filter_by_text_condition('rsi14 < 40')
historical_symbols = list(historical_symbols.index)

# Monitor these symbols in real-time for a buyer power greater than 2
while True:
    sleep(10)  # Check every 10 seconds
    current_power_symbols = RealTime().filter_by_text_condition('power_of_demand > 2')
    current_power_symbols = current_power_symbols['symbol'].tolist()
    for symbol in current_power_symbols:
        if symbol in historical_symbols:
            print(f'Historical RSI < 40 and current buyer power > 2 for {symbol}')

This approach allows traders to set up a system that alerts them when historically strong symbols show significant buying interest in the current market, providing a potential opportunity for trading.

Writing Conditions
A condition is a text string that defines the criteria for filtering stock data. Use the following syntax rules:

•  Utilize variables listed in the RealTimeVariables.xlsx and HistoryVariable.xlsx files.

•  Employ comparison operators: ==, !=, <, <=, >, >=.

•  Combine comparisons with logical operators: and, or.

•  Group comparisons with parentheses to alter operator precedence.

License
The pytse-filter project is licensed under the MIT License. Refer to the LICENSE file for details.