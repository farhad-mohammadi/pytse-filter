from pytse_filter import History

# History().download_summery() # فقط نیاز است برای بروز رسانی داده ها اجرا شود

# نمادهایی که RSI آنها کمتر از 50 باشد و  میانگین قدرت خریدار به فروشنده ی 10 روزه یآنها بیشتر از یک باشد
conditions = 'rsi < 50 and power_avg10 > 1'
df = History().filter_by_text_condition(conditions)
print(df)
# df.to_excel('my_filter.xlsx')

# نمادهای که در آنها خط K اندیکاتور StochAstic خط D را کراس کرده باشد

conditions = 'k < 30 and y_k < y_d and k > d'
df = History().filter_by_text_condition(conditions)
# print(df)
# df.to_excel('my_filter.xlsx')

# نمادهای که خط Tenkan خط Kijun را به بالا کراس کرده و ابر صعودی باشد
conditions = 'spana > spanb and y_tenkan < y_kijun and tenkan > kijun'
df = History().filter_by_text_condition(conditions)
print(df)
# df.to_excel('my_filter.xlsx')
