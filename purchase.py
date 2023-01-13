import pandas as pd
import os

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def get_data() -> pd.DataFrame:
	# Locate latest file
	file_name = '20221216_prijs_structuur.xlsx'
	
	# Read file data
	excel_obj = pd.read_excel(fp, sheet_name=None)
	df = excel_obj.get('INPUT')
	
	# Convert and set datetime obj to index
	df.Date = pd.to_datetime(df.Date)
	df.drapna(axis=0, how='all', subset='Date', inplace=True)
	df.set_index('Date', inplace=True)
	
	return df

def get_cost(currency='awg') -> pd.Series:
	"""Return total cost in AWG of LPG."""
	df = get_data()
	costs = df.loc[:, ['LPG', 'Freight & Insurance', 'Import tax', 'Handeling']]
	total_cost = costs.sum(axis=1)
	
	if currency == 'usd':
		return total_cost / 1.8279
	return total_cost

def get_quantity(unit='tons') -> pd.Series:
	df = get_data()
	if unit == 'kilos':
		return df.loc[:, 'Weight'] * 1_000
	if unit == 'pounds':
		return df.loc[:, 'Weight'] * 2_204.62262
	if unit == 'gallons':
		return df.loc[:, 'Volume']
	if unit == 'liters':
		return df.loc[:, 'Volume'] * 3.78541178
	return df.loc[:, 'Weight']

def get_density() -> pd.Series:
	"""Return density in Kg/m3 of LPG."""
	df = get_data()
	weight = df.loc[:, 'Weight'] * 1_000
	volume = df.loc[:, 'Volume'] * 3.78541178
	
	return weight / volume * 1_000

def get_cost_per_unit(currency, unit) -> pd.Series:
	series = get_cost(currency) / get_quantity(unit)
	series.name = 'cogs'
	return series

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
if __name__ == '__main__':
	
	cuurrency = 'awg'
	unit = 'kilos'
	print(get_cost_per_unit(currency, unit))
