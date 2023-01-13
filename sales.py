import pandas as pd
import purchase 

file_name = 'data_sales.csv'
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def fetch_constents(col_name: str) -> int:
	contents = {
		100: ['old_HSH 100 lb', 'new_HSH 100 lb', 'HSH 100 lb', 'COM 100 lb'],
		 60: ['HSH 60 lb', 'HSH 60 COM'],
		 20: ['COM 20 lb'],
		  7: ['CAMP GAS']
	}
	
	for k, v in contents.items():
		if col_name in v:
			return k
	return 1

def get_data(file_name: str) -> pd.DataFrame:
	"""Returns Sales data per unit."""
	df = pd.read_csv(file_name)
	# Convert and assign datetime obj to index
	df['Date'] = pd.to_datetime(df.iloc[:, 0], format='%Y%m%d')
	df.set_index('Date', inplace=True)
	df = df.drop('Unnamed: 0', axis=1)
	df['HSH 100 lb'] = df['old_HSH 100 lb'] + df['new_HSH 100 lb'].fillna(0)
	
	return df

def to_kilos(df: pd.DataFrame, col_name: str) -> pd.Series:
	"""Return Series converted into kilos."""
	lb2kg = 2.20462262
	contents = fetch_contents(col_name)
	density = purchase.get_density().mean()
	
	if not any([col_name in ['HSH BULK', 'COM BULK', 'MOTOR FUEL']]):
		return df.loc[:, col_name] * contents * lb2kg
	
	return df.loc[:, col_name] * (density / 1_000)

def to_liters(df: pd.DataFrame, col_name: str) -> pd.Series:
	"""Return Series converted into liters."""
	density = purchase.get_density().mean()
	
	if not any([col_name in ['HSH BULK', 'COM BULK', 'MOTOR FUEL']]):
		kilos = to_kilos(df, col_name)
		liters = kilos / (density / 1_000)
		return liters
	
	return df.loc[:, col_name]

def to_pounds(df: pd.DataFrame, col_name: str) -> pd.Series:
	"""Return Series converted to U.S. pounds."""
	kg2lb = 2.20462262
	kilos = to_kilos(df, col_name)
	return kilos * kg2lb

def to_gallons(df: pd.DataFrame, col_name: str) -> pd.Series:
	"""Return Series converted into U.S. gallons."""
	L2gallons = 1 / 3.785
	liters = to_liters(df, col_name)
	return liters * L2gallons

def get_prices(currency='awg'):
	dct = {
		'date': ['20220101', '20220307', '20220903', '20221115'],
		# HSH
		'HSH 100 lb': [46.38, 46.38, 46.38, 60.00],
		'HSH BULK': [.52, .52, .52, .66],
		'HSH 60 lb': [27.83, 27.83, 27.83, 36],
		# COM
		'COM 20 lb': [24, 25.5, 25.5, 25.5],
		'COM 60 lb': [86.5, 95, 95, 95],
		'COM 100 lb': [144, 158.5, 158.5, 158.5],
		'COM MIX': [1.44, 1.59, 1.59, 1.59],
		'COM BULK': [1.59, 1.75, 1.75, 1.75],
		'MOTOR FUEL': [1.3, 1.45, 1.55, 1.5]
	}
	
	prices = pd.DataFrame(dct)
	prices.date = pd.to_datetime(prices.date)
	prices.set_index('date', inplace=True)
	
	if currency == 'usd':
		return prices / 1.75
	
	return prices

def get_revenue(col_name: str , currency: str) -> pd.Series:
	quantity = get_data(file_name)
	prices = get_prices(currency)
	
	df = pd.concat([prices.loc[:, col_name], quantity.loc[:, col_name]], axis=1)
	df.columns = ['price', 'quantity']
	df.loc[:, 'price'] = df.loc[:, 'price'].ffill()
	
	revenue = df.price * df.quantity
	return revenue

def get_quantity(col_name: str, unit: str) -> pd.Series:
	dct = {
		'pounds': to_pounds,
		'kilos': to_kilos,
		'gallons': to_gallons,
		'liters': to_liters
	}
	df = get_data(file_name)
	return dct.get(unit)(df, col_name)

def get_price_per_unit(skew: str, currency: str, unit: str) -> pd.Series:
	price_per_unit = get_revenue(skew, currency) / get_quantity(skew, unit)
	price_per_name.name = 'revenue'
	return price_per_unit
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

if __name__ == '__main__':
	
	skew = 'HSH 100 lb'
	currency = 'awg'
	unit = 'pounds'
	
	print(get_price_per_unit(skew, currency, unit))
