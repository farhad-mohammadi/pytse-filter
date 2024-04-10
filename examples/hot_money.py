from pytse_filter import RealTime
from time import sleep

thereshold_in_money = 1_000_000_000 # یک میلیارد ریال
past_data = None
while past_data is None:
    past_data = RealTime().get_all_stocks_data()

while True:
    sleep(10)
    current_data = RealTime().get_all_stocks_data()
    if current_data is None:
        continue
    df = current_data[['buy_i_value', 'buy_i_count']] - past_data[['buy_i_value', 'buy_i_count']]
    df['symbol'] = current_data['symbol']
    df['in_money_per_capita'] = df['buy_i_value'] / df['buy_i_count']
    df = df.loc[df['in_money_per_capita'] > thereshold_in_money]
    if len(df) != 0:
        #می توان نمادها را به شبکه های اجتماعی ارسال کرد
        print(df)
    past_data =current_data
    