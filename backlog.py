import pandas as pd
from datetime import datetime, timedelta

def get_backlog_data(route: str, years: list) -> pd.DataFrame:
	fp_back = 'data_backlog.csv'
	fp_deli = 'data_delivered.csv'

	df_back = pd.read_csv(fp_back)
	df_deli = pd.read_csv(fp_deli)

	df_back.date = pd.to_datetime(df_back.date, format='%Y%m%d')
	df_back.set_index('date', inplace=True)

	df_deli.date = pd.to_datetime(df_deli.date, format='%Y%m%d')
	df_deli.set_index('date', inplace=True)

	freq = 'W'
	df_sample_back = df_back.resample(freq).sum()
	df_sample_deli = df_deli.resample(freq).sum()

	main_back = df_sample_back #.drop('Unnamed: 8', axis=1)
	main_deli = df_sample_deli #.drop('Unnamed: 8', axis=1)

# 	if freq == 'M':
# 		main_back.index = [date - timedelta(date.day - 1) for date in main_back.index]
# 		main_deli.index = [date - timedelta(date.day - 1) for date in main_deli.index]
    
	main_back.index.name = 'Date'
	main_deli.index.name = 'Date'
	
	main_back['all'] = main_back.sum(axis=1)
	main_deli['all'] = main_deli.sum(axis=1)
	
	backlog_time = main_back / main_deli
	
	years = sorted(years)
	return backlog_time[route].loc[f'{years[0]}-01-01': f'{years[-1]}-12-31']
 
