from pytse_filter import RealTime
from time import time
import sys

market = RealTime()
sell_queue_symbols = market.filter_by_text_condition('pl == tmin')
if len(sell_queue_symbols) == 0:
    print('There are no sell queues')
    sys .exit()

sell_queue_symbols = sell_queue_symbols['symbol'].tolist()
print(sell_queue_symbols)
while True:
    if int(time()) % 10 != 0:
        continue
    reload_sell_queue_symbols = market.filter_by_text_condition('pl == tmin')
    if reload_sell_queue_symbols is None: 
        continue
    reload_sell_queue_symbols = reload_sell_queue_symbols['symbol'].tolist()
    for sym in sell_queue_symbols:
        if not sym in reload_sell_queue_symbols:
            print(f'Damage sell queue in {sym}')
    sell_queue_symbols = reload_sell_queue_symbols