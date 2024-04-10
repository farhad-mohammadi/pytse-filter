from pytse_filter import History, RealTime
from time import time

# History().download_summery() # شب قبل اجرا شده و سابقه بروز است

# نمادهایی که RSI آنها زیر 40 است و در زمان بازار قدرت بیشتر از 2 میشود
my_symbols = History().filter_by_text_condition('rsi < 40')
my_symbols = list(my_symbols.index)
print(my_symbols)

while True:
    if time() % 10 != 0:
        continue
    power_symbols = RealTime().filter_by_text_condition('power_of_demand > 2')
    power_symbols = power_symbols['symbol'].tolist()
    for s in power_symbols:
        if s in my_symbols:
            print(s)