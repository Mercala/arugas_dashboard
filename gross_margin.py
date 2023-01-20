import pandas as pd
import numpy as np

import plotly.express as px
import plotly

import purchase
import sales_volume_price

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def graph(revenue: pd.Series, cogs: pd.Series, skew: str, currency: str, unit: str, legend: str) -> plotly.graph_objs.Figure:
  
	# Prep DataFrame
	df = pd.concat([revenue, cogs], axis=1)
	df = df.ffill()
	df['gross margin'] = df.revenue - df.cogs
  
	# Plot
	fig = px.line(
    	df, 
    	title=f'Gross margin {skew.title()}<br><sup>in {currency.upper()} per {unit.rstrip("s").title()}</sup>',
    	color_discrete_sequence = ['drakgrey', 'grey', 'green']
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
		showlegend=legend
	)
	
	fig.update_xaxes(title_font_family='Arial Narrow')
	
	return fig

def main() ->:
	
	cogs = purchase.get_cost_per_unit(currency, unit)
	revenue = sales_volume_price.get_price_per_unit(skew, currency, unit)
	
	fig = graph(revenue, cogs, skew, currency, unit, legend)
	
	return fig
