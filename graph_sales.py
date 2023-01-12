import pandas as pd
import numpy as np

import plotly.express as px
import plotly

from get_data import get_sales_data
import purchase

PATH = ''
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
def graph(monthly_sales: pd.Series, purchase_weight: pd.Series, toggle: str) -> plotly.graph_objs.Figure:
	# Prep Colours to highlight import data
	pallete_1 = np.repeat('#5a5a5a', 12)
	pallete_1[monthly_sales.loc[:, 'Commercial'].idxmax().month -1] = '#092638'
	
	pallete_2 = np.repeat('gray', 12)
	pallete_2[monthly_sales.loc[:, 'Household'].idxmax().month -1] = '#156563'
	
	# Plot monthly sales Stacked | Use barmode = 'group', to unstack
	fig = px.bar(
		monthly_sales,
		title='LPG Sales Volume',
		color_discrete_sequence = [pallete_1, pallete_2]
	)
	
	# Add Purchase history plot to bar chart | use line={} for a step line chart
	if toggle == 'ON':
		fig.add_scatter(
			x=purchase_weight.index,
			y=purchase_weight.values,
			line={
				'shape': 'hv',
				'color': '#ab8989'
			}
		)
	# Add name to the legend for the added step line chart
		fig.update_traces(
			name='Purchase',
			selector={
				'type': 'scatter'
			}
		)
		
	# Adjust x axis tick label format
	fig.update_xaxes(
		tickformat='%b\n%Y'
	)
	
	# Format hover data | only 'y' values
	fig.update_traces(
		hovertemplate='<b> %{y:.0f} </b>'
	)
	
	# Change y axis title
	fig.update_layout(
		hovermode='x',
		xaxis_title=None,
		yaxis_title='Metric Tons',
		font={
			'family': 'Arial Narrow',
			'size': 20
		}
	)
	
	# Change font for axis
	fig.update(
		title_font_family='Arial Narrow'
	)
	
	return fig

def main(toggle):
	monthly_sales = get_sales_data()
	purchase_weight = purchase.get_data().Weight
	
	return graph(monthly_sales, purchase_weight, toggle)

if __name__ == '__main__':
	
	main()
