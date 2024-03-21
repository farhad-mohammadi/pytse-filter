from pytse_filter import RealTime

# نمادهایی که در منفی قدرت خریدار به فروشنده بیشتر از یک دارند
conditions = 'pl < py and power_of_demand > 1'
df = RealTime().filter_by_text_condition(conditions)
print(df)
# df.to_excel('myfilter.xlsx') # می توان نتیجه را در فایل اکسل ذخیره کرد

# نمادهایی با قدرت خریدار به فروشنده بیشتر از 2 و سرانه خرید بیشتر از 30 میلیون
conditions = 'power_of_demand > 2 and buy_per_capita > 30'
df = RealTime().filter_by_text_condition(conditions)
print(df)
# df.to_excel('myfilter.xlsx') # می توان نتیجه را در فایل اکسل ذخیره کرد

# نمادهایی که درصد خرید حقیقی بیشتر از 80 درصد و فروش حقوقی بیشتر از 30 درصد باشد
conditions = 'ind_buy_ratio > 80 and cor_sell_ratio > 50'
df = RealTime().filter_by_text_condition(conditions)
print(df)
# df.to_excel('myfilter.xlsx') # می توان نتیجه را در فایل اکسل ذخیره کرد