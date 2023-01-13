import pandas as pd
import numpy as np

import plotly.express as px
import plotly

import purchase
import sales

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def graph(skew: str, currency: str, unit: str) -> plotly.graph_objs.Figure:
	cogs = purchase.get_cost_per_unit(currency, unit)
	revenue = sales.get_price_per_unit(skew, currency, unit)
  
	# Prep DataFrame
	df = pd.concat([revenue, cogs], axis=1)
	df = df.ffill()
	df['gross margin'] = df.revenue - df.cogs
  
	# Plot
	fig = px.line(
    	df, 
    	title=f'Gross margin {skew.title()}<br><sup>in {currency.upper()} per {unit.rstrip("s").title()}</sup>',
    	color_discrete_sequence = ['#092672', '#0b5672', 'green']
  	)
  
	fig.update_xaxes(
		tickformat='%b\n%Y'
	)
	
	fig.update_traces(
		hovertemplate='<b> %{y:.2f} </b>'
	)
	
	fig.update_layout(
		hovermode='x',
		xaxis_title=None,
		yaxis_title=None,
		font={
			'family': 'Arial Narrow',
			'size': 20
		},
		legend={
		    'yanchor': "bottom",
		    'y': -0.99,
		    'xanchor': "left",
		    'x': 0.01
		}
	)
	
	fig.update_xaxes(title_font_family='Arial Narrow')
	
	return fig
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

if __name__ == '__main__':
	
	currency = 'awg'
	unit = 'liters'
	skew = 'COM BULK'
	
	fig = graph(skew, currency, unit)
	
	fig.show()
