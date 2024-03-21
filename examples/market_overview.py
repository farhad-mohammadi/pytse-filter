from pytse_filter import RealTime, RealTimeCondition
import sys

buy_queue_condition = RealTimeCondition('pl == tmax')
sell_queue_condition = RealTimeCondition('pl == tmin')
positive_conditions = RealTimeCondition('pl < tmax and plp > 1')
negative_conditions = RealTimeCondition('pl > tmin and plp < -1')
zero_condition = RealTimeCondition('plp <= 1 and plp >= -1')

market_data = RealTime()
market_data.download()
if not market_data.download_status:
    print("can't download data')")
    sys.exit()

market_data.condition = buy_queue_condition
buy_queue_symbols = market_data.filter_by_obj_condition(update_data= False)

market_data.condition = sell_queue_condition
sell_queue_symbols = market_data.filter_by_obj_condition(update_data= False)

market_data.condition = positive_conditions
positive_symbols = market_data.filter_by_obj_condition(update_data= False)

market_data.condition = negative_conditions
negative_symbols = market_data.filter_by_obj_condition(update_data= False)

market_data.condition = zero_condition
zero_symbols = market_data.filter_by_obj_condition(update_data= False)

symbols_total = len(buy_queue_symbols) + len(sell_queue_symbols) + len(positive_symbols) + len(negative_symbols) + len(zero_symbols)
msg = f"""بازار در یک نگاه:
از مجموع {symbols_total} نماد
{len(buy_queue_symbols)} نماد در صف خرید
{len(sell_queue_symbols)} نماد در صف فروش
{len(positive_symbols)} نماد در محدوده ی مثبت
{len(negative_symbols)} نماد در محدوده ی منفی
{len(zero_symbols)} نماد در محدوده ی صفر تابلو در حال معامله هستند."""

print(msg) # You can send the text to your social networks.
