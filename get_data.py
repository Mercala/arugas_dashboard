import pandas as pd
from datetime import datetime, timedelta

lb2mt = 1 / 2_204.62262
L2mt = 1 / 3.78541 * 4.25 / 2_204.62262

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def get_sales_data() -> pd.DataFrame:
	file_name_sales = 'data_sales.csv'
	
	# Read CSV
	df = pd.read_csv(file_name)
	
	# Prep DataFrame
	df.Date = pd.to_datetime(df.iloc[:, 0], format='%Y%m%d')
	df.set_index('Date', inplace=True)
	
	# Convert units
	# Household
	total_HSH_100lb = df.loc[:, ['old_HSH 100 lb', 'new_HSH 100 lb']].sum(axis=1) * 100 * lb2mt
	total_HSH_60lb = df.loc[:, 'HSH 60 lb'] * 60 * lb2mt
	total_HSH_mix = df.loc[:, 'HSH MIX'] * lb2mt
	total_HSH_bulk = df['HSH BULK'] * L2mt
	
	# Commercial
	total_COM_100lb = df.loc[:, 'COM 100 lb'] * 100 * lb2mt
	total_COM_20lb = df.loc[:, 'COM 20 lb'] * 20 * lb2mt
	total_COM_60lb = df.loc[:, 'COM 60 lb'] * 60 * lb2mt
	total_COM_mix = df.loc[:, 'COM MIX'] * lb2mt
	total_CAMP_GAS = df.loc[:, 'CAMP GAS'] * 7 * lb2mt
	total_COM_motor = df.loc[:, 'MOTOR FUEL'] * L2mt
	total_COM_bulk = df.loc[:, 'COM BULK'] * L2mt
	
	# Sum Columns
	HSH = round(total_HSH_60lb + total_HSH_100lb + total_HSH_mix + total_HSH_bulk)
	HSH.name = 'Household'
	COM = round(total_COM_100lb + total_COM_20lb + total_COM_60lb + total_COM_mix + total_CAMP_GAS + total_COM_motor + total_COM_bulk)
	COM.name = 'Commercial'
	
	# Concatenate pd.Series
	sales = pd.concat([COM, HSH], axis=1)
	monthly_sales = sales.resample('M').sum()
	# Recast date to 1st day of the month to ensure proper placement of bars in chart
	monthly_sales.index = [date - timedelta(date.day - 1) for date in monthly_sales.index]
	monthly_sales.index.name = 'Date'
	
	return monthly_sales

def get_backlog_data(year: str) -> pd.DataFrame:
	file_name = 'data_backlog.csv'
	
	# Read CSV
	df = pd.read_csv(file_name)
	
	# Convert Datetime obj & set index
	df.date = pd.to_datetime(df.date, format='%Y%m%d')
	df.set_index('date', inpalce=True)
	
	# Sum all orders into Series
	orders = df.iloc[:, :8].sum(axis=1)
	orders.name = 'total_orders'
	
	# Get all delivered into Series
	deliver = df.loc[:, 'Delivered']
	
	b = orders.resample('M').sum()
	a = deliver.resample('M').sum()
	
	ratio = round(a / b * 100, 1)
	ratio.name = 'Delivered'
	total = round(100 - ratio, 1)
	total.name = 'Total Orders'
	
	main = pd.concat([ratio, total], axis=1)
	# Adjust date for Bar plot placement
	main.index = [date - timedelta(date.day -1) for date in main.index]
	main.index.name = 'Date'
	
	return main.loc[year]
	
	
	
