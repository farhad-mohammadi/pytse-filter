pytse-filter: Tehran Stock Exchange Data Processing Library
Welcome to the pytse-filter library, a Python package designed for processing and analyzing Tehran Stock Exchange (TSE) symbol data through user-defined text filters. This library simplifies the task of filtering TSE data based on various conditions, making it an essential tool for traders and analysts.

Prerequisites
Before you begin, ensure you have the following:
•  Python 3.x installed on your system.

•  Required packages: pandas, pandas_ta, requests, and tqdm installed via pip.

Installation
Install pytse-filter easily using pip:

pip install pytse_filter

Or, for the latest version from the repository:

pip install git+https://github.com/farhad-mohammadi/pytse-filter.git

Alternatively, clone and install from the source:

git clone https://github.com/farhad-mohammadi/pytse-filter
cd pytse_filter
pip install .

Dependencies will be automatically resolved and installed.

Usage
pytse-filter is divided into two main components: Realtime and History. These cater to users ranging from beginners to professionals, providing tools for both real-time data processing and historical data analysis.

Realtime Filtering
For real-time data filtering, import the RealTime class and use it as follows:

from pytse_filter import RealTime

# Define your conditions
conditions = 'pl < py and power_of_demand > 1'

# Filter data based on conditions
df = RealTime().filter_by_text_condition(conditions)
print(df)

# Save results to Excel (optional)
df.to_excel('myfilter.xlsx')

Advanced Realtime Monitoring
Advanced users can continuously monitor symbol status changes:

from pytse_filter import RealTime
from time import sleep
import sys

# Initialize market data
market = RealTime()

# Fetch and monitor sell queue symbols
sell_queue_symbols = market.filter_by_text_condition('pl == tmin')
# ... rest of the advanced monitoring code ...

Historical Data Analysis
The History class allows for in-depth historical stock data analysis:

from pytse_filter import History

# Download and update data with the latest market information
History().download_summary()

# Apply filters based on technical indicators and patterns
conditions = 'rsi14 < 30 and macd > 0'
df = History().filter_by_text_condition(conditions)
print(df)

# Save filtered data (optional)
df.to_excel('filtered_symbols.xlsx')

Comprehensive Analysis
Combine realtime and historical data for a complete analysis setup:

from pytse_filter import History, RealTime
# ... code to combine and analyze data ...

Writing Conditions
Define criteria for filtering stock data using a simple text string format. Utilize variables from RealTimeVariables.xlsx and HistoryVariable.xlsx, and employ comparison and logical operators to create complex conditions.

License
pytse-filter is MIT licensed. See the LICENSE file for more details.

For the full user guide, examples, and advanced usage instructions, please refer to the user_guide.md included with this package.

Happy trading!