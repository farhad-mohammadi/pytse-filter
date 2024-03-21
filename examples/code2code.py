from pytse_filter import RealTime, RealTimeCondition

condition = RealTimeCondition(file_path= 'code2code.txt')
market = RealTime(condition)
symbols_df = market.filter_by_obj_condition()
# symbols_df.to_excel('code2code.xlsx')
print(symbols_df)